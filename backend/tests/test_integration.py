"""End-to-end integration tests for TaskFlow API."""

from fastapi.testclient import TestClient


# --- Health Check ---


class TestHealthCheck:
    """Tests for GET /."""

    def test_should_return_api_info(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TaskFlow API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"


# --- Full Task Lifecycle ---


class TestFullTaskLifecycle:
    """E2E test covering the complete task lifecycle."""

    def test_should_complete_full_task_lifecycle(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        # Create a task
        create_resp = client.post(
            "/tasks/",
            json={"title": "Lifecycle Task", "description": "E2E test", "priority": "high"},
            headers=auth_headers,
        )
        assert create_resp.status_code == 201
        task = create_resp.json()
        task_id = task["id"]
        assert task["title"] == "Lifecycle Task"
        assert task["status"] == "todo"

        # List tasks — should contain the created task
        list_resp = client.get("/tasks/")
        assert list_resp.status_code == 200
        tasks = list_resp.json()
        assert len(tasks) == 1
        assert tasks[0]["id"] == task_id

        # Get task by ID
        get_resp = client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Lifecycle Task"

        # Update the task
        update_resp = client.put(
            f"/tasks/{task_id}",
            json={"title": "Updated Task", "status": "done"},
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        updated = update_resp.json()
        assert updated["title"] == "Updated Task"
        assert updated["status"] == "done"

        # Delete the task
        delete_resp = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert delete_resp.status_code == 204

        # Verify task is gone (404)
        gone_resp = client.get(f"/tasks/{task_id}")
        assert gone_resp.status_code == 404


# --- Unauthorized Access ---


class TestUnauthorizedAccess:
    """Tests for unauthenticated requests."""

    def test_should_reject_create_without_token(self, client: TestClient) -> None:
        response = client.post("/tasks/", json={"title": "No Auth"})
        assert response.status_code == 401

    def test_should_reject_update_without_token(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.put(f"/tasks/{task_id}", json={"title": "Hacked"})
        assert response.status_code == 401

    def test_should_reject_delete_without_token(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 401


# --- Multiple Tasks ---


class TestMultipleTasks:
    """Tests for creating and listing multiple tasks."""

    def test_should_create_and_list_multiple_tasks(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        for i in range(3):
            resp = client.post(
                "/tasks/",
                json={"title": f"Task {i + 1}", "priority": "medium"},
                headers=auth_headers,
            )
            assert resp.status_code == 201

        list_resp = client.get("/tasks/")
        assert list_resp.status_code == 200
        tasks = list_resp.json()
        assert len(tasks) == 3
        titles = [t["title"] for t in tasks]
        assert "Task 1" in titles
        assert "Task 2" in titles
        assert "Task 3" in titles

    def test_should_support_pagination(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        for i in range(5):
            client.post(
                "/tasks/", json={"title": f"Task {i}"}, headers=auth_headers
            )
        response = client.get("/tasks/?skip=1&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


# --- Update Task Status ---


class TestUpdateTaskStatus:
    """Tests for updating task status."""

    def test_should_update_status_to_done(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Pending Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        assert create_resp.json()["status"] == "todo"

        update_resp = client.put(
            f"/tasks/{task_id}",
            json={"status": "done"},
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["status"] == "done"
        # Title should remain unchanged
        assert update_resp.json()["title"] == "Pending Task"

    def test_should_update_status_through_workflow(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        create_resp = client.post(
            "/tasks/", json={"title": "Workflow Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]
        assert create_resp.json()["status"] == "todo"

        # Move to in_progress
        resp1 = client.put(
            f"/tasks/{task_id}",
            json={"status": "in_progress"},
            headers=auth_headers,
        )
        assert resp1.json()["status"] == "in_progress"

        # Move to done
        resp2 = client.put(
            f"/tasks/{task_id}",
            json={"status": "done"},
            headers=auth_headers,
        )
        assert resp2.json()["status"] == "done"


# --- Ownership Authorization ---


class TestOwnershipAuthorization:
    """Tests for task ownership enforcement."""

    def test_should_forbid_non_owner_from_deleting(
        self,
        client: TestClient,
        auth_headers: dict,
        other_auth_headers: dict,
    ) -> None:
        # User A creates a task
        create_resp = client.post(
            "/tasks/", json={"title": "User A Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User B tries to delete it
        response = client.delete(f"/tasks/{task_id}", headers=other_auth_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to delete this task"

        # Verify task still exists
        get_resp = client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 200

    def test_should_forbid_non_owner_from_updating(
        self,
        client: TestClient,
        auth_headers: dict,
        other_auth_headers: dict,
    ) -> None:
        # User A creates a task
        create_resp = client.post(
            "/tasks/", json={"title": "User A Task"}, headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User B tries to update it
        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "Hacked Title"},
            headers=other_auth_headers,
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to update this task"

        # Verify task is unchanged
        get_resp = client.get(f"/tasks/{task_id}")
        assert get_resp.json()["title"] == "User A Task"


# --- 404 Not Found ---


class TestNotFound:
    """Tests for nonexistent resource access."""

    def test_should_return_404_for_get_nonexistent_task(
        self, client: TestClient
    ) -> None:
        response = client.get("/tasks/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_should_return_404_for_update_nonexistent_task(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        response = client.put(
            "/tasks/9999",
            json={"title": "Nope"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_should_return_404_for_delete_nonexistent_task(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        response = client.delete("/tasks/9999", headers=auth_headers)
        assert response.status_code == 404
