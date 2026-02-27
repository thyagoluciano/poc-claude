"""Unit tests for TaskFlow Pydantic schemas."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from taskflow.schemas import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    UserCreate,
    UserResponse,
)


# --- TaskCreate Tests ---


class TestTaskCreate:
    """Tests for TaskCreate schema."""

    def test_should_create_task_with_required_fields(self) -> None:
        task = TaskCreate(title="My Task")
        assert task.title == "My Task"
        assert task.description is None
        assert task.priority == "medium"

    def test_should_create_task_with_all_fields(self) -> None:
        task = TaskCreate(
            title="My Task",
            description="A detailed description",
            priority="high",
        )
        assert task.title == "My Task"
        assert task.description == "A detailed description"
        assert task.priority == "high"

    def test_should_reject_empty_title(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")
        assert "title" in str(exc_info.value)

    def test_should_reject_title_exceeding_max_length(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="a" * 201)
        assert "title" in str(exc_info.value)

    def test_should_accept_title_at_max_length(self) -> None:
        task = TaskCreate(title="a" * 200)
        assert len(task.title) == 200

    def test_should_reject_invalid_priority(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Task", priority="urgent")  # type: ignore[arg-type]
        assert "priority" in str(exc_info.value)

    def test_should_default_priority_to_medium(self) -> None:
        task = TaskCreate(title="Task")
        assert task.priority == "medium"


# --- TaskUpdate Tests ---


class TestTaskUpdate:
    """Tests for TaskUpdate schema."""

    def test_should_create_update_with_no_fields(self) -> None:
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.priority is None
        assert update.status is None

    def test_should_create_update_with_partial_fields(self) -> None:
        update = TaskUpdate(title="Updated Title")
        assert update.title == "Updated Title"
        assert update.description is None
        assert update.priority is None
        assert update.status is None

    def test_should_create_update_with_status_only(self) -> None:
        update = TaskUpdate(status="done")
        assert update.status == "done"
        assert update.title is None

    def test_should_create_update_with_all_fields(self) -> None:
        update = TaskUpdate(
            title="New Title",
            description="New description",
            priority="low",
            status="in_progress",
        )
        assert update.title == "New Title"
        assert update.description == "New description"
        assert update.priority == "low"
        assert update.status == "in_progress"

    def test_should_reject_empty_title_in_update(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(title="")
        assert "title" in str(exc_info.value)

    def test_should_reject_invalid_status(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(status="cancelled")  # type: ignore[arg-type]
        assert "status" in str(exc_info.value)

    def test_should_reject_invalid_priority_in_update(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(priority="critical")  # type: ignore[arg-type]
        assert "priority" in str(exc_info.value)


# --- TaskResponse Tests ---


class TestTaskResponse:
    """Tests for TaskResponse schema."""

    def test_should_create_response_with_all_fields(self) -> None:
        now = datetime.now()
        response = TaskResponse(
            id=1,
            title="Task",
            description="Description",
            priority="high",
            status="todo",
            created_at=now,
            updated_at=None,
            owner_id=42,
        )
        assert response.id == 1
        assert response.title == "Task"
        assert response.status == "todo"
        assert response.created_at == now
        assert response.updated_at is None
        assert response.owner_id == 42

    def test_should_support_from_attributes_config(self) -> None:
        assert TaskResponse.model_config.get("from_attributes") is True


# --- UserCreate Tests ---


class TestUserCreate:
    """Tests for UserCreate schema."""

    def test_should_create_user_with_valid_data(self) -> None:
        user = UserCreate(
            username="johndoe",
            email="john@example.com",
            password="securepass",
        )
        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.password == "securepass"

    def test_should_reject_short_username(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="ab",
                email="john@example.com",
                password="securepass",
            )
        assert "username" in str(exc_info.value)

    def test_should_reject_long_username(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="a" * 51,
                email="john@example.com",
                password="securepass",
            )
        assert "username" in str(exc_info.value)

    def test_should_reject_short_password(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="johndoe",
                email="john@example.com",
                password="short",
            )
        assert "password" in str(exc_info.value)

    def test_should_accept_password_at_min_length(self) -> None:
        user = UserCreate(
            username="johndoe",
            email="john@example.com",
            password="12345678",
        )
        assert len(user.password) == 8

    def test_should_reject_invalid_email(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="johndoe",
                email="not-an-email",
                password="securepass",
            )
        assert "email" in str(exc_info.value)

    def test_should_reject_missing_email(self) -> None:
        with pytest.raises(ValidationError):
            UserCreate(username="johndoe", password="securepass")  # type: ignore[call-arg]


# --- UserResponse Tests ---


class TestUserResponse:
    """Tests for UserResponse schema."""

    def test_should_create_response_with_all_fields(self) -> None:
        now = datetime.now()
        response = UserResponse(
            id=1,
            username="johndoe",
            email="john@example.com",
            created_at=now,
        )
        assert response.id == 1
        assert response.username == "johndoe"
        assert response.email == "john@example.com"
        assert response.created_at == now

    def test_should_support_from_attributes_config(self) -> None:
        assert UserResponse.model_config.get("from_attributes") is True
