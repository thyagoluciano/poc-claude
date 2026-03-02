"""Tests for database setup and models."""

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from taskflow.database import Base, SessionLocal, get_db
from taskflow.db_models import TaskModel, UserModel


def test_should_create_tables(engine) -> None:
    """Verify that all expected tables are created."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "tasks" in tables


def test_should_create_user(db_session) -> None:
    """Verify that a user can be created and persisted."""
    user = UserModel(
        email="test@example.com",
        username="testuser",
        hashed_password="fakehash123",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password == "fakehash123"
    assert user.created_at is not None


def test_should_create_task_with_owner(db_session) -> None:
    """Verify that a task can be created with an owner relationship."""
    user = UserModel(
        email="owner@example.com",
        username="owner",
        hashed_password="fakehash123",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task = TaskModel(
        title="Test Task",
        description="A test task",
        status="pending",
        priority="high",
        owner_id=user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.owner_id == user.id
    assert task.owner.username == "owner"
    assert task.created_at is not None

    # Verify relationship from user side
    db_session.refresh(user)
    assert len(user.tasks) == 1
    assert user.tasks[0].title == "Test Task"


def test_should_enforce_unique_email(db_session) -> None:
    """Verify that duplicate emails are rejected."""
    user1 = UserModel(
        email="duplicate@example.com",
        username="user1",
        hashed_password="fakehash123",
    )
    db_session.add(user1)
    db_session.commit()

    user2 = UserModel(
        email="duplicate@example.com",
        username="user2",
        hashed_password="fakehash456",
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_should_get_db_session() -> None:
    """Verify that get_db yields a working session."""
    gen = get_db()
    session = next(gen)
    assert session is not None
    assert isinstance(session, type(SessionLocal()))
    # Clean up the generator
    try:
        next(gen)
    except StopIteration:
        pass
