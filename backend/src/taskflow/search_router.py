"""Public search router for TaskFlow API."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .database import get_db
from .repositories import TaskRepository
from .schemas import TaskSearchResult

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/tasks", response_model=list[TaskSearchResult])
def search_tasks(
    q: str = Query(default="", max_length=200),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
) -> list[TaskSearchResult]:
    """Search tasks by title (case insensitive, partial match).

    This is a public endpoint that does not require authentication.

    Args:
        q: Search query string to match against task titles.
        skip: Number of results to skip for pagination.
        limit: Maximum number of results to return (1-50).
        db: Database session.

    Returns:
        List of tasks matching the query with owner info.
    """
    if not q.strip():
        return []

    repo = TaskRepository(db)
    return repo.search_by_title(q, skip=skip, limit=limit)
