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
        """Search results include owner username but not owner_id or email."""
        client.post(
            "/tasks",
            json={"title": "Task with owner"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "owner"})
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) == 1
        assert results[0]["owner"]["username"] == sample_user.username
        # owner_id and email should NOT be exposed in public search
        assert "owner_id" not in results[0]
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

    def test_should_escape_wildcard_percent(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Searching for '%' should not match all tasks (wildcard escaped)."""
        client.post(
            "/tasks",
            json={"title": "Normal task"},
            headers=auth_headers,
        )
        client.post(
            "/tasks",
            json={"title": "100% complete"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "%"})
        assert resp.status_code == 200
        results = resp.json()
        # Only the task with literal '%' in the title should match
        assert len(results) == 1
        assert results[0]["title"] == "100% complete"

    def test_should_escape_wildcard_underscore(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Searching for '_' should not match single-character wildcards."""
        client.post(
            "/tasks",
            json={"title": "A task"},
            headers=auth_headers,
        )
        client.post(
            "/tasks",
            json={"title": "Use snake_case naming"},
            headers=auth_headers,
        )

        resp = client.get("/search/tasks", params={"q": "_"})
        assert resp.status_code == 200
        results = resp.json()
        # Only the task with literal '_' in the title should match
        assert len(results) == 1
        assert results[0]["title"] == "Use snake_case naming"

    def test_should_respect_pagination_limit(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search respects the limit parameter."""
        for i in range(5):
            client.post(
                "/tasks",
                json={"title": f"Paginated task {i}"},
                headers=auth_headers,
            )

        resp = client.get("/search/tasks", params={"q": "Paginated", "limit": 2})
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_should_respect_pagination_skip(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Search respects the skip parameter."""
        for i in range(5):
            client.post(
                "/tasks",
                json={"title": f"Paginated task {i}"},
                headers=auth_headers,
            )

        resp = client.get(
            "/search/tasks", params={"q": "Paginated", "skip": 3, "limit": 50}
        )
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_should_reject_limit_above_max(
        self,
        client: TestClient,
    ) -> None:
        """Search rejects limit values above 50."""
        resp = client.get("/search/tasks", params={"q": "test", "limit": 51})
        assert resp.status_code == 422

    def test_should_reject_query_above_max_length(
        self,
        client: TestClient,
    ) -> None:
        """Search rejects query strings longer than 200 characters."""
        long_query = "a" * 201
        resp = client.get("/search/tasks", params={"q": long_query})
        assert resp.status_code == 422
