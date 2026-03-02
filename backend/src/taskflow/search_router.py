"""Public search router for TaskFlow API."""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from .database import get_db
from .db_models import TaskModel, UserModel

router = APIRouter(prefix="/search", tags=["search"])


class TaskOwnerInfo(BaseModel):
    """Public owner information returned in search results."""

    username: str

    model_config = ConfigDict(from_attributes=True)


class TaskSearchResult(BaseModel):
    """Schema for task search results with owner info."""

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    owner_id: int
    owner: TaskOwnerInfo

    model_config = ConfigDict(from_attributes=True)


@router.get("/tasks", response_model=list[TaskSearchResult])
def search_tasks(
    q: str = Query(default="", max_length=200),
    db: Session = Depends(get_db),
) -> list[TaskSearchResult]:
    """Search tasks by title (case insensitive, partial match).

    This is a public endpoint that does not require authentication.

    Args:
        q: Search query string to match against task titles.
        db: Database session.

    Returns:
        List of tasks matching the query with owner info.
    """
    if not q.strip():
        return []

    tasks = (
        db.query(TaskModel)
        .join(UserModel, TaskModel.owner_id == UserModel.id)
        .filter(TaskModel.title.ilike(f"%{q}%"))
        .all()
    )
    return tasks
