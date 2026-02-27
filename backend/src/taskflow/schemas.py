"""Pydantic schemas for the TaskFlow API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


# --- Task Schemas ---


class TaskBase(BaseModel):
    """Base schema for task data."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: Literal["low", "medium", "high"] = "medium"


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    status: Literal["todo", "in_progress", "done"] | None = None


class TaskResponse(TaskBase):
    """Schema for task responses returned by the API."""

    id: int
    status: str
    created_at: datetime
    updated_at: datetime | None = None
    owner_id: int

    model_config = {"from_attributes": True}


# --- User Schemas ---


class UserBase(BaseModel):
    """Base schema for user data."""

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(min_length=8)


class UserResponse(UserBase):
    """Schema for user responses returned by the API."""

    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
