"""Task endpoints router for TaskFlow API."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .db_models import TaskModel, UserModel
from .repositories import TaskRepository
from .schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[TaskModel]:
    """List all tasks with pagination."""
    return TaskRepository.list_all(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskModel:
    """Get a task by its ID.

    Raises:
        HTTPException: 404 if the task does not exist.
    """
    task = TaskRepository.get_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> TaskModel:
    """Create a new task owned by the authenticated user."""
    return TaskRepository.create(db, task_data, owner_id=current_user.id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> TaskModel:
    """Update a task. Only the task owner can update it.

    Raises:
        HTTPException: 404 if the task does not exist.
        HTTPException: 403 if the current user is not the owner.
    """
    task = TaskRepository.get_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task",
        )
    updated = TaskRepository.update(db, task_id, task_data)
    return updated  # type: ignore[return-value]


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    """Delete a task. Only the task owner can delete it.

    Raises:
        HTTPException: 404 if the task does not exist.
        HTTPException: 403 if the current user is not the owner.
    """
    task = TaskRepository.get_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task",
        )
    TaskRepository.delete(db, task_id)
