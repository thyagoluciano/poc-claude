"""Pydantic v2 schemas para validacao de dados da TaskFlow API."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TaskBase(BaseModel):
    """Schema base para tarefas."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: Literal["pending", "in_progress", "done"] = "pending"
    priority: Literal["low", "medium", "high"] = "medium"


class TaskCreate(TaskBase):
    """Schema para criacao de tarefas."""

    pass


class TaskUpdate(BaseModel):
    """Schema para atualizacao parcial de tarefas."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[Literal["pending", "in_progress", "done"]] = None
    priority: Optional[Literal["low", "medium", "high"]] = None


class TaskResponse(TaskBase):
    """Schema de resposta para tarefas."""

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskSearchOwner(BaseModel):
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
    owner: TaskSearchOwner

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Schema base para usuarios."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema para criacao de usuarios."""

    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """Schema de resposta para usuarios."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
