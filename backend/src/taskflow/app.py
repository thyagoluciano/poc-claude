"""FastAPI application setup for TaskFlow API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth_router import router as auth_router
from .database import Base, engine
from .search_router import router as search_router
from .task_router import router as task_router

app = FastAPI(title="TaskFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(search_router)
app.include_router(task_router)


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on application startup."""
    Base.metadata.create_all(bind=engine)
