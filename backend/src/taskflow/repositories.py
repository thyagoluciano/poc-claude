"""Repository layer with CRUD operations for TaskFlow API."""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db_models import TaskModel, UserModel
from .schemas import TaskCreate, TaskUpdate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TaskRepository:
    """CRUD operations for tasks."""

    @staticmethod
    def create(db: Session, task: TaskCreate, owner_id: int) -> TaskModel:
        """Create a new task owned by the given user."""
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            priority=task.priority,
            owner_id=owner_id,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_by_id(db: Session, task_id: int) -> TaskModel | None:
        """Return a task by its ID, or None if not found."""
        return db.query(TaskModel).filter(TaskModel.id == task_id).first()

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[TaskModel]:
        """Return a paginated list of all tasks."""
        return db.query(TaskModel).offset(skip).limit(limit).all()

    @staticmethod
    def list_by_owner(db: Session, owner_id: int) -> list[TaskModel]:
        """Return all tasks owned by a specific user."""
        return db.query(TaskModel).filter(TaskModel.owner_id == owner_id).all()

    @staticmethod
    def update(db: Session, task_id: int, task: TaskUpdate) -> TaskModel | None:
        """Update a task with the provided fields. Returns None if not found."""
        db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if db_task is None:
            return None
        update_data = task.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete(db: Session, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if db_task is None:
            return False
        db.delete(db_task)
        db.commit()
        return True


class UserRepository:
    """CRUD operations for users."""

    @staticmethod
    def create(db: Session, user: UserCreate) -> UserModel:
        """Create a new user with a hashed password."""
        hashed_password = pwd_context.hash(user.password)
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> UserModel | None:
        """Return a user by their ID, or None if not found."""
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> UserModel | None:
        """Return a user by their username, or None if not found."""
        return db.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verify a plain-text password against a hashed password."""
        return pwd_context.verify(plain, hashed)
