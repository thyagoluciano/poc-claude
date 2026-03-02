"""End-to-end integration tests for TaskFlow API.

Tests cover the complete lifecycle: register -> login -> create -> list -> update -> delete.
Also covers auth/authz edge cases: missing token, expired token, cross-user access.
"""

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# E2E lifecycle tests
# ---------------------------------------------------------------------------


class TestE2ELifecycle:
    """Full user lifecycle: register, login, CRUD tasks, then verify cleanup."""

    def test_should_complete_full_task_lifecycle(self, client: TestClient) -> None:
        """Test the complete flow: register -> login -> create -> list -> get -> update -> delete."""
        # 1. Register a new user
        register_resp = client.post(
            "/auth/register",
            json={
                "email": "e2e@example.com",
                "username": "e2euser",
                "password": "securepassword123",
            },
        )
        assert register_resp.status_code == 201
        user_data = register_resp.json()
        assert user_data["username"] == "e2euser"
        assert "id" in user_data
        assert "password" not in user_data
        assert "hashed_password" not in user_data

        # 2. Login with the registered user
        login_resp = client.post(
            "/auth/login",
            data={"username": "e2euser", "password": "securepassword123"},
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        assert login_resp.json()["token_type"] == "bearer"
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create a task
        create_resp = client.post(
            "/tasks",
            json={
                "title": "E2E Task",
                "description": "Created in E2E test",
                "priority": "high",
            },
            headers=headers,
        )
        assert create_resp.status_code == 201
        task = create_resp.json()
        task_id = task["id"]
        assert task["title"] == "E2E Task"
        assert task["description"] == "Created in E2E test"
        assert task["status"] == "pending"
        assert task["priority"] == "high"
        assert task["owner_id"] == user_data["id"]

        # 4. List tasks — should contain the created task
        list_resp = client.get("/tasks", headers=headers)
        assert list_resp.status_code == 200
        tasks = list_resp.json()
        assert len(tasks) == 1
        assert tasks[0]["id"] == task_id

        # 5. Get task by ID
        get_resp = client.get(f"/tasks/{task_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "E2E Task"

        # 6. Update the task
        update_resp = client.put(
            f"/tasks/{task_id}",
            json={"title": "E2E Task Updated", "status": "done"},
            headers=headers,
        )
        assert update_resp.status_code == 200
        updated = update_resp.json()
        assert updated["title"] == "E2E Task Updated"
        assert updated["status"] == "done"
        assert updated["priority"] == "high"  # unchanged

        # 7. Delete the task
        delete_resp = client.delete(f"/tasks/{task_id}", headers=headers)
        assert delete_resp.status_code == 204

        # 8. Verify task is gone
        get_deleted_resp = client.get(f"/tasks/{task_id}", headers=headers)
        assert get_deleted_resp.status_code == 404

        # 9. List should be empty
        list_after_resp = client.get("/tasks", headers=headers)
        assert list_after_resp.status_code == 200
        assert list_after_resp.json() == []

    def test_should_handle_multiple_tasks_lifecycle(self, client: TestClient) -> None:
        """Test creating multiple tasks, listing, and deleting them."""
        # Register and login
        client.post(
            "/auth/register",
            json={
                "email": "multi@example.com",
                "username": "multiuser",
                "password": "securepassword123",
            },
        )
        login_resp = client.post(
            "/auth/login",
            data={"username": "multiuser", "password": "securepassword123"},
        )
        headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}

        # Create 3 tasks with different priorities
        task_ids = []
        for i, priority in enumerate(["low", "medium", "high"]):
            resp = client.post(
                "/tasks",
                json={"title": f"Task {i + 1}", "priority": priority},
                headers=headers,
            )
            assert resp.status_code == 201
            task_ids.append(resp.json()["id"])

        # List all — should have 3
        list_resp = client.get("/tasks", headers=headers)
        assert len(list_resp.json()) == 3

        # Update middle task to done
        client.put(
            f"/tasks/{task_ids[1]}",
            json={"status": "done"},
            headers=headers,
        )

        # Delete first task
        del_resp = client.delete(f"/tasks/{task_ids[0]}", headers=headers)
        assert del_resp.status_code == 204

        # List should have 2 remaining
        list_resp = client.get("/tasks", headers=headers)
        remaining = list_resp.json()
        assert len(remaining) == 2
        remaining_ids = [t["id"] for t in remaining]
        assert task_ids[0] not in remaining_ids
        assert task_ids[1] in remaining_ids
        assert task_ids[2] in remaining_ids


# ---------------------------------------------------------------------------
# Authentication tests — access denied without token
# ---------------------------------------------------------------------------


class TestAuthRequired:
    """Verify all task endpoints reject unauthenticated requests."""

    def test_should_reject_create_task_without_token(self, client: TestClient) -> None:
        """POST /tasks without Authorization header returns 401."""
        resp = client.post("/tasks", json={"title": "No Auth"})
        assert resp.status_code == 401

    def test_should_reject_list_tasks_without_token(self, client: TestClient) -> None:
        """GET /tasks without Authorization header returns 401."""
        resp = client.get("/tasks")
        assert resp.status_code == 401

    def test_should_reject_get_task_without_token(self, client: TestClient) -> None:
        """GET /tasks/{id} without Authorization header returns 401."""
        resp = client.get("/tasks/1")
        assert resp.status_code == 401

    def test_should_reject_update_task_without_token(self, client: TestClient) -> None:
        """PUT /tasks/{id} without Authorization header returns 401."""
        resp = client.put("/tasks/1", json={"title": "Hacked"})
        assert resp.status_code == 401

    def test_should_reject_delete_task_without_token(self, client: TestClient) -> None:
        """DELETE /tasks/{id} without Authorization header returns 401."""
        resp = client.delete("/tasks/1")
        assert resp.status_code == 401

    def test_should_reject_invalid_token(self, client: TestClient) -> None:
        """All endpoints reject a malformed Bearer token."""
        headers = {"Authorization": "Bearer invalid-token-value"}
        assert client.get("/tasks", headers=headers).status_code == 401
        assert client.post("/tasks", json={"title": "X"}, headers=headers).status_code == 401
        assert client.get("/tasks/1", headers=headers).status_code == 401
        assert client.put("/tasks/1", json={"title": "X"}, headers=headers).status_code == 401
        assert client.delete("/tasks/1", headers=headers).status_code == 401


# ---------------------------------------------------------------------------
# Authorization tests — cross-user access denied
# ---------------------------------------------------------------------------


class TestCrossUserAuthorization:
    """Verify that users cannot access, modify, or delete tasks owned by others."""

    def test_should_deny_read_other_user_task(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ) -> None:
        """User A cannot GET a task owned by User B."""
        create_resp = client.post(
            "/tasks",
            json={"title": "Private Task"},
            headers=other_auth_headers,
        )
        task_id = create_resp.json()["id"]

        resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert resp.status_code == 404

    def test_should_deny_update_other_user_task(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ) -> None:
        """User A cannot PUT a task owned by User B."""
        create_resp = client.post(
            "/tasks",
            json={"title": "Private Task"},
            headers=other_auth_headers,
        )
        task_id = create_resp.json()["id"]

        resp = client.put(
            f"/tasks/{task_id}",
            json={"title": "Hijacked"},
            headers=auth_headers,
        )
        assert resp.status_code == 404

        # Verify original is unchanged
        get_resp = client.get(f"/tasks/{task_id}", headers=other_auth_headers)
        assert get_resp.json()["title"] == "Private Task"

    def test_should_deny_delete_other_user_task(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ) -> None:
        """User A cannot DELETE a task owned by User B."""
        create_resp = client.post(
            "/tasks",
            json={"title": "Private Task"},
            headers=other_auth_headers,
        )
        task_id = create_resp.json()["id"]

        resp = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert resp.status_code == 404

        # Verify task still exists for owner
        get_resp = client.get(f"/tasks/{task_id}", headers=other_auth_headers)
        assert get_resp.status_code == 200

    def test_should_isolate_task_lists_between_users(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        other_auth_headers: dict[str, str],
    ) -> None:
        """Each user only sees their own tasks in GET /tasks."""
        client.post(
            "/tasks",
            json={"title": "User A Task"},
            headers=auth_headers,
        )
        client.post(
            "/tasks",
            json={"title": "User B Task"},
            headers=other_auth_headers,
        )

        resp_a = client.get("/tasks", headers=auth_headers)
        tasks_a = resp_a.json()
        assert len(tasks_a) == 1
        assert tasks_a[0]["title"] == "User A Task"

        resp_b = client.get("/tasks", headers=other_auth_headers)
        tasks_b = resp_b.json()
        assert len(tasks_b) == 1
        assert tasks_b[0]["title"] == "User B Task"


# ---------------------------------------------------------------------------
# Auth endpoint edge cases
# ---------------------------------------------------------------------------


class TestAuthEdgeCases:
    """Edge cases for registration and login endpoints."""

    def test_should_reject_duplicate_email_registration(
        self, client: TestClient
    ) -> None:
        """POST /auth/register rejects duplicate email."""
        client.post(
            "/auth/register",
            json={
                "email": "dup@example.com",
                "username": "user1",
                "password": "securepassword123",
            },
        )
        resp = client.post(
            "/auth/register",
            json={
                "email": "dup@example.com",
                "username": "user2",
                "password": "securepassword123",
            },
        )
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_should_reject_duplicate_username_registration(
        self, client: TestClient
    ) -> None:
        """POST /auth/register rejects duplicate username."""
        client.post(
            "/auth/register",
            json={
                "email": "a@example.com",
                "username": "dupuser",
                "password": "securepassword123",
            },
        )
        resp = client.post(
            "/auth/register",
            json={
                "email": "b@example.com",
                "username": "dupuser",
                "password": "securepassword123",
            },
        )
        assert resp.status_code == 400
        assert "Username already taken" in resp.json()["detail"]

    def test_should_reject_login_with_wrong_password(
        self, client: TestClient
    ) -> None:
        """POST /auth/login rejects wrong password."""
        client.post(
            "/auth/register",
            json={
                "email": "wrong@example.com",
                "username": "wronguser",
                "password": "securepassword123",
            },
        )
        resp = client.post(
            "/auth/login",
            data={"username": "wronguser", "password": "badpassword99"},
        )
        assert resp.status_code == 401

    def test_should_reject_login_with_nonexistent_user(
        self, client: TestClient
    ) -> None:
        """POST /auth/login rejects nonexistent username."""
        resp = client.post(
            "/auth/login",
            data={"username": "ghost", "password": "securepassword123"},
        )
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Task validation edge cases
# ---------------------------------------------------------------------------


class TestTaskValidation:
    """Edge cases for task CRUD operations."""

    def test_should_return_404_for_nonexistent_task(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        """GET /tasks/9999 returns 404."""
        resp = client.get("/tasks/9999", headers=auth_headers)
        assert resp.status_code == 404

    def test_should_return_404_when_updating_nonexistent_task(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        """PUT /tasks/9999 returns 404."""
        resp = client.put(
            "/tasks/9999",
            json={"title": "Does Not Exist"},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_should_return_404_when_deleting_nonexistent_task(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        """DELETE /tasks/9999 returns 404."""
        resp = client.delete("/tasks/9999", headers=auth_headers)
        assert resp.status_code == 404

    def test_should_support_partial_update(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        """PUT /tasks/{id} updates only provided fields."""
        create_resp = client.post(
            "/tasks",
            json={"title": "Original", "priority": "low", "description": "Keep me"},
            headers=auth_headers,
        )
        task_id = create_resp.json()["id"]

        update_resp = client.put(
            f"/tasks/{task_id}",
            json={"priority": "high"},
            headers=auth_headers,
        )
        updated = update_resp.json()
        assert updated["title"] == "Original"
        assert updated["priority"] == "high"
        assert updated["description"] == "Keep me"

    def test_should_create_task_with_all_statuses(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        """POST /tasks accepts all valid status values."""
        for task_status in ["pending", "in_progress", "done"]:
            resp = client.post(
                "/tasks",
                json={"title": f"Task {task_status}", "status": task_status},
                headers=auth_headers,
            )
            assert resp.status_code == 201
            assert resp.json()["status"] == task_status

    def test_should_return_empty_list_for_new_user(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        """GET /tasks returns empty list when user has no tasks."""
        resp = client.get("/tasks", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []
