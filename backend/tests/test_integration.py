"""Integration tests for TaskFlow API endpoints."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from taskflow.auth import create_access_token, hash_password
from taskflow.auth_router import router as auth_router
from taskflow.database import get_db
from taskflow.db_models import UserModel
from taskflow.task_router import router as task_router


@pytest.fixture
def app(db_session: Session) -> FastAPI:
    """Create a FastAPI test application with both routers."""
    test_app = FastAPI(title="TaskFlow API")
    test_app.include_router(auth_router)
    test_app.include_router(task_router)

    def override_get_db():
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
    """Create another user for ownership tests."""
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
    """Return authorization headers for the sample user."""
    token = create_access_token(data={"sub": sample_user.username})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_auth_headers(other_user: UserModel) -> dict[str, str]:
    """Return authorization headers for the other user."""
    token = create_access_token(data={"sub": other_user.username})
    return {"Authorization": f"Bearer {token}"}


# --- POST /tasks ---


def test_should_create_task(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that POST /tasks creates a new task for the authenticated user."""
    response = client.post(
        "/tasks",
        json={"title": "My Task", "description": "A test task"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Task"
    assert data["description"] == "A test task"
    assert data["status"] == "pending"
    assert data["priority"] == "medium"
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data


def test_should_create_task_with_custom_status_and_priority(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that POST /tasks accepts custom status and priority."""
    response = client.post(
        "/tasks",
        json={
            "title": "Urgent Task",
            "status": "in_progress",
            "priority": "high",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"


def test_should_reject_create_task_without_auth(client: TestClient) -> None:
    """Test that POST /tasks requires authentication."""
    response = client.post(
        "/tasks",
        json={"title": "Unauthorized Task"},
    )
    assert response.status_code == 401


# --- GET /tasks ---


def test_should_list_user_tasks(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that GET /tasks returns only tasks belonging to the authenticated user."""
    client.post(
        "/tasks",
        json={"title": "Task 1"},
        headers=auth_headers,
    )
    client.post(
        "/tasks",
        json={"title": "Task 2"},
        headers=auth_headers,
    )

    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_should_not_list_other_user_tasks(
    client: TestClient,
    auth_headers: dict[str, str],
    other_auth_headers: dict[str, str],
) -> None:
    """Test that GET /tasks does not return tasks from other users."""
    client.post(
        "/tasks",
        json={"title": "My Task"},
        headers=auth_headers,
    )
    client.post(
        "/tasks",
        json={"title": "Other Task"},
        headers=other_auth_headers,
    )

    response = client.get("/tasks", headers=auth_headers)
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "My Task"


def test_should_return_empty_list_when_no_tasks(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that GET /tasks returns empty list when user has no tasks."""
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


# --- GET /tasks/{task_id} ---


def test_should_get_task_by_id(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that GET /tasks/{task_id} returns the task if owned by user."""
    create_response = client.post(
        "/tasks",
        json={"title": "Specific Task"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"


def test_should_return_404_for_nonexistent_task(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that GET /tasks/{task_id} returns 404 for nonexistent task."""
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_should_return_404_for_other_user_task(
    client: TestClient,
    auth_headers: dict[str, str],
    other_auth_headers: dict[str, str],
) -> None:
    """Test that GET /tasks/{task_id} returns 404 for task owned by another user."""
    create_response = client.post(
        "/tasks",
        json={"title": "Other's Task"},
        headers=other_auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404


# --- PUT /tasks/{task_id} ---


def test_should_update_task(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that PUT /tasks/{task_id} updates the task."""
    create_response = client.post(
        "/tasks",
        json={"title": "Old Title"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New Title", "status": "done"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "done"


def test_should_partial_update_task(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that PUT /tasks/{task_id} supports partial updates."""
    create_response = client.post(
        "/tasks",
        json={"title": "Original", "priority": "low"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"priority": "high"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Original"
    assert data["priority"] == "high"


def test_should_return_404_when_updating_other_user_task(
    client: TestClient,
    auth_headers: dict[str, str],
    other_auth_headers: dict[str, str],
) -> None:
    """Test that PUT /tasks/{task_id} returns 404 for task owned by another user."""
    create_response = client.post(
        "/tasks",
        json={"title": "Other's Task"},
        headers=other_auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=auth_headers,
    )
    assert response.status_code == 404


# --- DELETE /tasks/{task_id} ---


def test_should_delete_task(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that DELETE /tasks/{task_id} removes the task."""
    create_response = client.post(
        "/tasks",
        json={"title": "To Delete"},
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404


def test_should_return_404_when_deleting_nonexistent_task(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test that DELETE /tasks/{task_id} returns 404 for nonexistent task."""
    response = client.delete("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_should_return_404_when_deleting_other_user_task(
    client: TestClient,
    auth_headers: dict[str, str],
    other_auth_headers: dict[str, str],
) -> None:
    """Test that DELETE /tasks/{task_id} returns 404 for task owned by another user."""
    create_response = client.post(
        "/tasks",
        json={"title": "Other's Task"},
        headers=other_auth_headers,
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404
