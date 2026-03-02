"""Task CRUD router for TaskFlow API."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .db_models import UserModel
from .repositories import TaskRepository
from .schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """Create a new task for the authenticated user.

    Args:
        task_data: Validated task creation data.
        db: Database session.
        current_user: The authenticated user.

    Returns:
        The created task.
    """
    repo = TaskRepository(db)
    task = repo.create(task_data, owner_id=current_user.id)
    return task


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> list[TaskResponse]:
    """List all tasks belonging to the authenticated user.

    Args:
        db: Database session.
        current_user: The authenticated user.

    Returns:
        List of tasks owned by the user.
    """
    repo = TaskRepository(db)
    return repo.list_by_owner(current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """Get a specific task by ID.

    Args:
        task_id: The task primary key.
        db: Database session.
        current_user: The authenticated user.

    Returns:
        The task if found and owned by the user.

    Raises:
        HTTPException: If the task is not found or not owned by the user.
    """
    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """Update an existing task.

    Args:
        task_id: The task primary key.
        task_data: Validated partial update data.
        db: Database session.
        current_user: The authenticated user.

    Returns:
        The updated task.

    Raises:
        HTTPException: If the task is not found or not owned by the user.
    """
    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    updated_task = repo.update(task_id, task_data)
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    """Delete a task.

    Args:
        task_id: The task primary key.
        db: Database session.
        current_user: The authenticated user.

    Raises:
        HTTPException: If the task is not found or not owned by the user.
    """
    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    repo.delete(task_id)
