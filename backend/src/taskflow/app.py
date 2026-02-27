"""FastAPI application for TaskFlow API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth_router import router as auth_router
from .database import create_tables
from .task_router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create database tables on startup."""
    create_tables()
    yield


app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def root() -> dict:
    """Return API information."""
    return {
        "name": "TaskFlow API",
        "version": "1.0.0",
        "docs": "/docs",
    }
