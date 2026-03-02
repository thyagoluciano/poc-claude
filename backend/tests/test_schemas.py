"""Testes para os schemas Pydantic da TaskFlow API."""

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


class TestTaskSchemas:
    """Testes para schemas de Task."""

    def test_should_create_valid_task(self) -> None:
        """Verifica criacao de task com dados validos."""
        task = TaskCreate(title="Minha tarefa", description="Descricao da tarefa")
        assert task.title == "Minha tarefa"
        assert task.description == "Descricao da tarefa"
        assert task.status == "pending"
        assert task.priority == "medium"

    def test_should_reject_empty_title(self) -> None:
        """Verifica rejeicao de task com titulo vazio."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_should_create_task_with_all_fields(self) -> None:
        """Verifica criacao de task com todos os campos."""
        task = TaskCreate(
            title="Task completa",
            description="Desc",
            status="in_progress",
            priority="high",
        )
        assert task.status == "in_progress"
        assert task.priority == "high"

    def test_should_reject_invalid_status(self) -> None:
        """Verifica rejeicao de status invalido."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Task", status="invalid")

    def test_should_reject_invalid_priority(self) -> None:
        """Verifica rejeicao de prioridade invalida."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Task", priority="urgent")

    def test_should_reject_title_too_long(self) -> None:
        """Verifica rejeicao de titulo com mais de 200 caracteres."""
        with pytest.raises(ValidationError):
            TaskCreate(title="a" * 201)

    def test_should_create_task_update_partial(self) -> None:
        """Verifica criacao de TaskUpdate com campos parciais."""
        update = TaskUpdate(title="Novo titulo")
        assert update.title == "Novo titulo"
        assert update.description is None
        assert update.status is None
        assert update.priority is None

    def test_should_create_task_update_empty(self) -> None:
        """Verifica criacao de TaskUpdate sem nenhum campo."""
        update = TaskUpdate()
        assert update.title is None
        assert update.status is None

    def test_should_create_task_response_from_attributes(self) -> None:
        """Verifica que TaskResponse suporta from_attributes."""
        now = datetime.now()
        response = TaskResponse(
            id=1,
            owner_id=1,
            title="Task",
            status="pending",
            priority="medium",
            created_at=now,
            updated_at=now,
        )
        assert response.id == 1
        assert response.owner_id == 1
        assert response.created_at == now


class TestUserSchemas:
    """Testes para schemas de User."""

    def test_should_create_valid_user(self) -> None:
        """Verifica criacao de usuario com dados validos."""
        user = UserCreate(
            email="user@example.com",
            username="testuser",
            password="securepass123",
        )
        assert user.email == "user@example.com"
        assert user.username == "testuser"
        assert user.password == "securepass123"

    def test_should_reject_short_password(self) -> None:
        """Verifica rejeicao de senha com menos de 8 caracteres."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="user@example.com",
                username="testuser",
                password="short",
            )
        assert "String should have at least 8 character" in str(exc_info.value)

    def test_should_reject_invalid_email(self) -> None:
        """Verifica rejeicao de email invalido."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="not-an-email",
                username="testuser",
                password="securepass123",
            )
        assert "value is not a valid email address" in str(exc_info.value)

    def test_should_reject_short_username(self) -> None:
        """Verifica rejeicao de username com menos de 3 caracteres."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="user@example.com",
                username="ab",
                password="securepass123",
            )

    def test_should_reject_long_username(self) -> None:
        """Verifica rejeicao de username com mais de 50 caracteres."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="user@example.com",
                username="a" * 51,
                password="securepass123",
            )

    def test_should_create_user_response_from_attributes(self) -> None:
        """Verifica que UserResponse suporta from_attributes."""
        now = datetime.now()
        response = UserResponse(
            id=1,
            email="user@example.com",
            username="testuser",
            created_at=now,
        )
        assert response.id == 1
        assert response.created_at == now
