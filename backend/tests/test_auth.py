"""Tests for JWT authentication module."""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt

from taskflow.auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    decode_access_token,
    get_current_user,
)
from taskflow.db_models import UserModel


def test_should_create_access_token() -> None:
    """Test that create_access_token returns a valid JWT string."""
    token = create_access_token(data={"sub": "testuser"})
    assert isinstance(token, str)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "exp" in payload


def test_should_decode_valid_token() -> None:
    """Test that decode_access_token correctly decodes a valid token."""
    token = create_access_token(data={"sub": "testuser"})
    payload = decode_access_token(token)
    assert payload["sub"] == "testuser"


def test_should_reject_expired_token() -> None:
    """Test that decode_access_token raises HTTPException for expired tokens."""
    from fastapi import HTTPException

    expire = datetime.now(timezone.utc) - timedelta(minutes=1)
    token = jwt.encode(
        {"sub": "testuser", "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    with pytest.raises(HTTPException) as exc_info:
        decode_access_token(token)
    assert exc_info.value.status_code == 401


def test_should_register_user(client: TestClient) -> None:
    """Test that POST /auth/register creates a new user."""
    response = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_should_login_user(client: TestClient, sample_user: UserModel) -> None:
    """Test that POST /auth/login returns a valid access token."""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_should_reject_wrong_password(client: TestClient, sample_user: UserModel) -> None:
    """Test that POST /auth/login rejects incorrect password."""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_should_reject_duplicate_user(client: TestClient, sample_user: UserModel) -> None:
    """Test that POST /auth/register rejects duplicate email or username."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "anotheruser",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

    response = client.post(
        "/auth/register",
        json={
            "email": "another@example.com",
            "username": "testuser",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_should_get_current_user(
    app: FastAPI, sample_user: UserModel
) -> None:
    """Test that get_current_user dependency extracts user from JWT token."""
    from fastapi import Depends

    @app.get("/test-auth")
    def protected_route(user: UserModel = Depends(get_current_user)):
        return {"username": user.username, "email": user.email}

    client = TestClient(app)
    token = create_access_token(data={"sub": sample_user.username})

    response = client.get(
        "/test-auth",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
