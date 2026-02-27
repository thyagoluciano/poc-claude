"""Tests for database configuration and ORM models."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from taskflow.database import Base, get_db
from taskflow.db_models import TaskModel, UserModel


@pytest.fixture()
def db_session() -> Session:
    """Create an in-memory SQLite database session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# --- Table creation tests ---


def test_should_create_users_table(db_session: Session) -> None:
    """Verify that the 'users' table is created with expected columns."""
    inspector = inspect(db_session.bind)
    tables = inspector.get_table_names()
    assert "users" in tables

    columns = {col["name"] for col in inspector.get_columns("users")}
    assert columns == {"id", "username", "email", "hashed_password", "created_at"}


def test_should_create_tasks_table(db_session: Session) -> None:
    """Verify that the 'tasks' table is created with expected columns."""
    inspector = inspect(db_session.bind)
    tables = inspector.get_table_names()
    assert "tasks" in tables

    columns = {col["name"] for col in inspector.get_columns("tasks")}
    expected = {
        "id",
        "title",
        "description",
        "priority",
        "status",
        "created_at",
        "updated_at",
        "owner_id",
    }
    assert columns == expected


# --- Insertion tests ---


def test_should_insert_user(db_session: Session) -> None:
    """Verify that a user can be inserted and retrieved."""
    user = UserModel(
        username="alice",
        email="alice@example.com",
        hashed_password="hashed123",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert isinstance(user.created_at, datetime)


def test_should_insert_task(db_session: Session) -> None:
    """Verify that a task can be inserted with default values."""
    user = UserModel(
        username="bob",
        email="bob@example.com",
        hashed_password="hashed456",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task = TaskModel(
        title="My first task",
        description="A test task",
        owner_id=user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert task.title == "My first task"
    assert task.priority == "medium"
    assert task.status == "todo"
    assert task.owner_id == user.id
    assert isinstance(task.created_at, datetime)


# --- Relationship tests ---


def test_should_relate_user_to_tasks(db_session: Session) -> None:
    """Verify that a user's tasks relationship works bidirectionally."""
    user = UserModel(
        username="carol",
        email="carol@example.com",
        hashed_password="hashed789",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task1 = TaskModel(title="Task A", owner_id=user.id)
    task2 = TaskModel(title="Task B", owner_id=user.id)
    db_session.add_all([task1, task2])
    db_session.commit()

    db_session.refresh(user)
    assert len(user.tasks) == 2
    assert {t.title for t in user.tasks} == {"Task A", "Task B"}


def test_should_access_owner_from_task(db_session: Session) -> None:
    """Verify that a task can navigate back to its owner."""
    user = UserModel(
        username="dave",
        email="dave@example.com",
        hashed_password="hashedabc",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task = TaskModel(title="Owner test", owner_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.owner is not None
    assert task.owner.username == "dave"


# --- get_db dependency test ---


def test_should_yield_session_from_get_db() -> None:
    """Verify that get_db yields a Session and closes it."""
    gen = get_db()
    session = next(gen)
    assert isinstance(session, Session)
    try:
        gen.send(None)
    except StopIteration:
        pass
