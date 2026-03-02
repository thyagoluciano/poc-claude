"""Repository layer for CRUD operations on TaskFlow models."""

from datetime import datetime, timezone

import bcrypt
from sqlalchemy.orm import Session

from .db_models import TaskModel, UserModel
from .schemas import TaskCreate, TaskUpdate


def _hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


class TaskRepository:
    """Handles CRUD operations for tasks."""

    def __init__(self, db: Session) -> None:
        """Initialize with a database session."""
        self.db = db

    def create(self, task_data: TaskCreate, owner_id: int) -> TaskModel:
        """Create a new task.

        Args:
            task_data: Validated task creation data.
            owner_id: ID of the task owner.

        Returns:
            The newly created task model.
        """
        db_task = TaskModel(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            owner_id=owner_id,
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: int) -> TaskModel | None:
        """Retrieve a task by its ID.

        Args:
            task_id: The task primary key.

        Returns:
            The task model or None if not found.
        """
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def list_all(self) -> list[TaskModel]:
        """Retrieve all tasks.

        Returns:
            A list of all task models.
        """
        return list(self.db.query(TaskModel).all())

    def list_by_owner(self, owner_id: int) -> list[TaskModel]:
        """Retrieve all tasks belonging to a specific owner.

        Args:
            owner_id: The owner's user ID.

        Returns:
            A list of task models owned by the user.
        """
        return list(
            self.db.query(TaskModel).filter(TaskModel.owner_id == owner_id).all()
        )

    def update(self, task_id: int, task_data: TaskUpdate) -> TaskModel | None:
        """Update an existing task with partial data.

        Args:
            task_id: The task primary key.
            task_data: Validated partial update data.

        Returns:
            The updated task model or None if not found.
        """
        db_task = self.get_by_id(task_id)
        if db_task is None:
            return None

        update_fields = task_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def search_by_title(
        self, query: str, skip: int = 0, limit: int = 50
    ) -> list[TaskModel]:
        """Search tasks by title with case insensitive partial matching.

        LIKE wildcards (% and _) in the query are escaped before searching.

        Args:
            query: Search string to match against task titles.
            skip: Number of results to skip (offset).
            limit: Maximum number of results to return (capped at 50).

        Returns:
            A list of matching task models with owner relationship loaded.
        """
        escaped = query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        return list(
            self.db.query(TaskModel)
            .join(UserModel, TaskModel.owner_id == UserModel.id)
            .filter(TaskModel.title.ilike(f"%{escaped}%", escape="\\"))
            .offset(skip)
            .limit(min(limit, 50))
            .all()
        )

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The task primary key.

        Returns:
            True if the task was deleted, False if not found.
        """
        db_task = self.get_by_id(task_id)
        if db_task is None:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True


class UserRepository:
    """Handles CRUD operations for users."""

    def __init__(self, db: Session) -> None:
        """Initialize with a database session."""
        self.db = db

    def create(self, username: str, email: str, password: str) -> UserModel:
        """Create a new user with a hashed password.

        Args:
            username: The unique username.
            email: The user's email address.
            password: The plain-text password (will be hashed).

        Returns:
            The newly created user model.
        """
        hashed_password = _hash_password(password)
        db_user = UserModel(
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> UserModel | None:
        """Retrieve a user by ID.

        Args:
            user_id: The user primary key.

        Returns:
            The user model or None if not found.
        """
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_username(self, username: str) -> UserModel | None:
        """Retrieve a user by username.

        Args:
            username: The unique username to search for.

        Returns:
            The user model or None if not found.
        """
        return (
            self.db.query(UserModel).filter(UserModel.username == username).first()
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a hashed password.

        Args:
            plain_password: The password to check.
            hashed_password: The stored bcrypt hash.

        Returns:
            True if the password matches, False otherwise.
        """
        return _verify_password(plain_password, hashed_password)
