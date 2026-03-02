"""Shared test fixtures for TaskFlow tests."""

from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from taskflow.auth import create_access_token, hash_password
from taskflow.auth_router import router as auth_router
from taskflow.database import Base, get_db
from taskflow.db_models import UserModel
from taskflow.task_router import router as task_router

SQLITE_IN_MEMORY_URL = "sqlite://"


@pytest.fixture
def engine():
    """Create an in-memory SQLite engine for tests."""
    test_engine = create_engine(
        SQLITE_IN_MEMORY_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def db_session(engine) -> Generator[Session, None, None]:
    """Provide a transactional test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def app(db_session: Session) -> FastAPI:
    """Create a FastAPI test application with all routers and overridden DB."""
    test_app = FastAPI(title="TaskFlow API")
    test_app.include_router(auth_router)
    test_app.include_router(task_router)

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    test_app.dependency_overrides[get_db] = override_get_db
    return test_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test HTTP client."""
    return TestClient(app)


@pytest.fixture
def sample_user(db_session: Session) -> UserModel:
    """Create a sample user in the test database."""
    user = UserModel(
        email="test@example.com",
        username="testuser",
        hashed_password=hash_password("securepassword123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def other_user(db_session: Session) -> UserModel:
    """Create a second user for cross-user authorization tests."""
    user = UserModel(
        email="other@example.com",
        username="otheruser",
        hashed_password=hash_password("securepassword123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(sample_user: UserModel) -> dict[str, str]:
    """Return Authorization headers with a valid JWT for sample_user."""
    token = create_access_token(data={"sub": sample_user.username})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_auth_headers(other_user: UserModel) -> dict[str, str]:
    """Return Authorization headers with a valid JWT for other_user."""
    token = create_access_token(data={"sub": other_user.username})
    return {"Authorization": f"Bearer {token}"}
