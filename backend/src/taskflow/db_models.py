"""SQLAlchemy ORM models for TaskFlow API."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def _utcnow() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


class UserModel(Base):
    """User account model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    tasks: Mapped[list["TaskModel"]] = relationship("TaskModel", back_populates="owner")


class TaskModel(Base):
    """Task model owned by a user."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(10), default="medium")
    status: Mapped[str] = mapped_column(String(20), default="todo")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, onupdate=_utcnow
    )
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="tasks")
