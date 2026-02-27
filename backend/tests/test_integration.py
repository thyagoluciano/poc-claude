"""Integration tests for TaskFlow API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from taskflow.app import app
from taskflow.database import Base, get_db


@pytest.fixture()
def client():
    """Create a test client with an in-memory SQLite database."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client: TestClient) -> dict:
    """Register a user and return auth headers with JWT token."""
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "securepass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def other_auth_headers(client: TestClient) -> dict:
    """Register a second user and return auth headers."""
    client.post(
        "/auth/register",
        json={
            "username": "otheruser",
            "email": "other@example.com",
            "password": "securepass123",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "otheruser", "password": "securepass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- Root Endpoint ---


class TestRootEndpoint:
    """Tests for GET /."""

    def test_should_return_api_info(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TaskFlow API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"


# --- Task Endpoints ---


class TestCreateTask:
    """Tests for POST /tasks."""

    def test_should_create_task_when_authenticated(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        response = client.post(
            "/tasks/",
            json={"title": "My Task", "description": "Details", "priority": "high"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "My Task"
        assert data["description"] == "Details"
        assert data["priority"] == "high"
        assert data["status"] == "todo"
        assert "id" in data
        assert "owner_id" in data

    def test_should_reject_unauthenticated_create(self, client: TestClient) -> None:
        response = client.post(
            "/tasks/",
            json={"title": "My Task"},
        )
        assert response.status_code == 401


class TestListTasks:
    """Tests for GET /tasks."""

    def test_should_return_empty_list(self, client: TestClient) -> None:
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_should_return_created_tasks(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        client.post(
            "/tasks/", json={"title": "Task 1"}, headers=auth_headers
        )
        client.post(
            "/tasks/", json={"title": "Task 2"}, headers=auth_headers
        )
        response = client.get("/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_should_support_pagination(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        for i in range(5):
            client.post(
                "/tasks/", json={"title": f"Task {i}"}, headers=auth_headers
            )
        response = client.get("/tasks/?skip=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestGetTask:
    """Tests for GET /tasks/{task_id}."""

    def test_should_return_task_by_id(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "My Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "My Task"

    def test_should_return_404_for_nonexistent_task(
        self, client: TestClient
    ) -> None:
        response = client.get("/tasks/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


class TestUpdateTask:
    """Tests for PUT /tasks/{task_id}."""

    def test_should_update_task_as_owner(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Old Title"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "New Title", "status": "done"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["status"] == "done"

    def test_should_reject_update_by_non_owner(
        self,
        client: TestClient,
        auth_headers: dict,
        other_auth_headers: dict,
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "Hacked"},
            headers=other_auth_headers,
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to update this task"

    def test_should_reject_unauthenticated_update(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "Hacked"},
        )
        assert response.status_code == 401

    def test_should_return_404_for_nonexistent_task(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        response = client.put(
            "/tasks/9999",
            json={"title": "Nope"},
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /tasks/{task_id}."""

    def test_should_delete_task_as_owner(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "To Delete"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 204

        get_resp = client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 404

    def test_should_reject_delete_by_non_owner(
        self,
        client: TestClient,
        auth_headers: dict,
        other_auth_headers: dict,
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.delete(
            f"/tasks/{task_id}", headers=other_auth_headers
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to delete this task"

    def test_should_reject_unauthenticated_delete(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 401

    def test_should_return_404_for_nonexistent_task(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        response = client.delete("/tasks/9999", headers=auth_headers)
        assert response.status_code == 404
