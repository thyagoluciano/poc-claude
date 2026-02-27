"""Tests for JWT authentication and auth endpoints."""

from datetime import timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from taskflow.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from taskflow.auth_router import router
from taskflow.database import Base, get_db


@pytest.fixture()
def db_engine():
    """Create an in-memory SQLite engine shared across threads."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(db_engine) -> Session:
    """Create a database session for testing."""
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_engine, db_session: Session) -> TestClient:
    """Create a FastAPI test client with database dependency override."""
    app = FastAPI()
    app.include_router(router)

    def _override_get_db() -> Session:
        session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _override_get_db
    return TestClient(app)


# --- Password hashing tests ---


def test_should_hash_and_verify_password() -> None:
    """Verify that a password can be hashed and verified."""
    hashed = hash_password("mysecretpassword")
    assert hashed != "mysecretpassword"
    assert verify_password("mysecretpassword", hashed) is True


def test_should_reject_wrong_password() -> None:
    """Verify that an incorrect password fails verification."""
    hashed = hash_password("correct-password")
    assert verify_password("wrong-password", hashed) is False


# --- Token creation and decoding tests ---


def test_should_create_and_decode_token() -> None:
    """Verify that a token can be created and decoded with correct claims."""
    token = create_access_token(data={"sub": "alice"})
    payload = decode_access_token(token)
    assert payload["sub"] == "alice"
    assert "exp" in payload


def test_should_create_token_with_custom_expiry() -> None:
    """Verify that a token respects custom expiration delta."""
    token = create_access_token(
        data={"sub": "bob"}, expires_delta=timedelta(minutes=5)
    )
    payload = decode_access_token(token)
    assert payload["sub"] == "bob"


def test_should_reject_expired_token() -> None:
    """Verify that an expired token raises HTTPException 401."""
    token = create_access_token(
        data={"sub": "carol"}, expires_delta=timedelta(seconds=-1)
    )
    with pytest.raises(Exception) as exc_info:
        decode_access_token(token)
    assert exc_info.value.status_code == 401


def test_should_reject_invalid_token() -> None:
    """Verify that a tampered token raises HTTPException 401."""
    with pytest.raises(Exception) as exc_info:
        decode_access_token("not-a-valid-token")
    assert exc_info.value.status_code == 401


# --- Register endpoint tests ---


def test_should_register_user(client: TestClient) -> None:
    """Verify that POST /auth/register creates a user and returns profile."""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_should_reject_duplicate_registration(client: TestClient) -> None:
    """Verify that registering with an existing username/email returns 400."""
    payload = {
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "securepassword123",
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


# --- Login endpoint tests ---


def test_should_login_with_valid_credentials(client: TestClient) -> None:
    """Verify that POST /auth/login returns an access token."""
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "securepassword123",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify the token is valid and contains the correct subject
    payload = decode_access_token(data["access_token"])
    assert payload["sub"] == "loginuser"


def test_should_reject_login_with_wrong_password(client: TestClient) -> None:
    """Verify that login with wrong password returns 401."""
    client.post(
        "/auth/register",
        json={
            "username": "wrongpw",
            "email": "wrongpw@example.com",
            "password": "correctpassword123",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "wrongpw", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_should_reject_login_with_nonexistent_user(client: TestClient) -> None:
    """Verify that login with nonexistent user returns 401."""
    response = client.post(
        "/auth/login",
        data={"username": "ghost", "password": "doesnotmatter"},
    )
    assert response.status_code == 401
