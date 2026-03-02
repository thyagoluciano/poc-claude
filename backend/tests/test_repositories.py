"""Tests for the repository layer."""

import pytest
from sqlalchemy.orm import Session

from taskflow.repositories import TaskRepository, UserRepository
from taskflow.schemas import TaskCreate, TaskUpdate


@pytest.fixture
def user_repo(db_session: Session) -> UserRepository:
    """Provide a UserRepository backed by the test session."""
    return UserRepository(db_session)


@pytest.fixture
def task_repo(db_session: Session) -> TaskRepository:
    """Provide a TaskRepository backed by the test session."""
    return TaskRepository(db_session)


@pytest.fixture
def sample_user(user_repo: UserRepository):
    """Create and return a sample user for task tests."""
    return user_repo.create(
        username="testuser",
        email="test@example.com",
        password="securepassword123",
    )


# ---- Task tests ----


def test_should_create_task(task_repo: TaskRepository, sample_user) -> None:
    """Creating a task persists it with the correct attributes."""
    task_data = TaskCreate(title="My Task", description="A description")
    task = task_repo.create(task_data, owner_id=sample_user.id)

    assert task.id is not None
    assert task.title == "My Task"
    assert task.description == "A description"
    assert task.status == "pending"
    assert task.priority == "medium"
    assert task.owner_id == sample_user.id


def test_should_get_task_by_id(task_repo: TaskRepository, sample_user) -> None:
    """A task can be retrieved by its primary key."""
    task_data = TaskCreate(title="Find me")
    created = task_repo.create(task_data, owner_id=sample_user.id)

    found = task_repo.get_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.title == "Find me"


def test_should_return_none_for_missing_task(task_repo: TaskRepository) -> None:
    """Getting a non-existent task returns None."""
    assert task_repo.get_by_id(9999) is None


def test_should_list_all_tasks(task_repo: TaskRepository, sample_user) -> None:
    """list_all returns every task in the database."""
    task_repo.create(TaskCreate(title="Task 1"), owner_id=sample_user.id)
    task_repo.create(TaskCreate(title="Task 2"), owner_id=sample_user.id)

    tasks = task_repo.list_all()
    assert len(tasks) == 2


def test_should_list_tasks_by_owner(
    task_repo: TaskRepository, user_repo: UserRepository, sample_user
) -> None:
    """list_by_owner only returns tasks belonging to the given owner."""
    other_user = user_repo.create(
        username="other", email="other@example.com", password="password1234"
    )
    task_repo.create(TaskCreate(title="Owner task"), owner_id=sample_user.id)
    task_repo.create(TaskCreate(title="Other task"), owner_id=other_user.id)

    owner_tasks = task_repo.list_by_owner(sample_user.id)
    assert len(owner_tasks) == 1
    assert owner_tasks[0].title == "Owner task"


def test_should_update_task(task_repo: TaskRepository, sample_user) -> None:
    """Updating a task changes only the provided fields."""
    task_data = TaskCreate(title="Original")
    created = task_repo.create(task_data, owner_id=sample_user.id)

    updated = task_repo.update(
        created.id, TaskUpdate(title="Updated", status="done")
    )
    assert updated is not None
    assert updated.title == "Updated"
    assert updated.status == "done"
    assert updated.priority == "medium"  # unchanged


def test_should_return_none_when_updating_missing_task(
    task_repo: TaskRepository,
) -> None:
    """Updating a non-existent task returns None."""
    assert task_repo.update(9999, TaskUpdate(title="Nope")) is None


def test_should_delete_task(task_repo: TaskRepository, sample_user) -> None:
    """Deleting a task removes it from the database."""
    task_data = TaskCreate(title="Delete me")
    created = task_repo.create(task_data, owner_id=sample_user.id)

    assert task_repo.delete(created.id) is True
    assert task_repo.get_by_id(created.id) is None


def test_should_return_false_when_deleting_missing_task(
    task_repo: TaskRepository,
) -> None:
    """Deleting a non-existent task returns False."""
    assert task_repo.delete(9999) is False


# ---- User tests ----


def test_should_create_user(user_repo: UserRepository) -> None:
    """Creating a user persists it with a hashed password."""
    user = user_repo.create(
        username="newuser", email="new@example.com", password="mypassword1"
    )

    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.hashed_password != "mypassword1"  # password is hashed


def test_should_get_user_by_username(user_repo: UserRepository) -> None:
    """A user can be retrieved by username."""
    user_repo.create(
        username="lookup", email="lookup@example.com", password="password123"
    )

    found = user_repo.get_by_username("lookup")
    assert found is not None
    assert found.username == "lookup"


def test_should_return_none_for_missing_username(user_repo: UserRepository) -> None:
    """Getting a non-existent username returns None."""
    assert user_repo.get_by_username("ghost") is None


def test_should_verify_password(user_repo: UserRepository) -> None:
    """verify_password returns True for the correct password."""
    user = user_repo.create(
        username="authuser", email="auth@example.com", password="correcthorse"
    )

    assert user_repo.verify_password("correcthorse", user.hashed_password) is True


def test_should_reject_wrong_password(user_repo: UserRepository) -> None:
    """verify_password returns False for an incorrect password."""
    user = user_repo.create(
        username="authuser2", email="auth2@example.com", password="correcthorse"
    )

    assert user_repo.verify_password("wrongpassword", user.hashed_password) is False
