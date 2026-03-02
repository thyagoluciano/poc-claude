"""Tests for the public search endpoint."""

from fastapi.testclient import TestClient


class TestSearchTasks:
    """Tests for GET /search/tasks endpoint."""

    def test_should_search_tasks_by_title(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search finds tasks matching the query in title."""
        client.post(
            "/tasks",
            json={"title": "Buy groceries", "priority": "low"},
            headers=auth_headers,
        )
        client.post(
            "/tasks",
            json={"title": "Fix bug in API", "priority": "high"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "groceries"})
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["title"] == "Buy groceries"

    def test_should_return_empty_for_no_match(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search returns empty list when no tasks match the query."""
        client.post(
            "/tasks",
            json={"title": "Some task"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "nonexistent"})
        assert resp.status_code == 200
        assert resp.json() == []

    def test_should_search_without_auth(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search endpoint works without authentication headers."""
        client.post(
            "/tasks",
            json={"title": "Public search task"},
            headers=auth_headers,
        )

        # No auth headers -- should still work
        resp = client.get("/search/tasks", params={"q": "Public"})
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["title"] == "Public search task"

    def test_should_return_owner_info(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        sample_user,
    ) -> None:
        """Search results include owner username."""
        client.post(
            "/tasks",
            json={"title": "Task with owner"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "owner"})
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["owner_id"] == sample_user.id
        assert results[0]["owner"]["username"] == sample_user.username
        # Email should NOT be exposed in public search
        assert "email" not in results[0]["owner"]

    def test_should_search_case_insensitive(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search is case insensitive."""
        client.post(
            "/tasks",
            json={"title": "Important Meeting"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "important meeting"})
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_should_return_empty_for_blank_query(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search returns empty list for blank query string."""
        client.post(
            "/tasks",
            json={"title": "Some task"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": ""})
        assert resp.status_code == 200
        assert resp.json() == []
