"""Unit tests for TaskFlow repository layer."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from taskflow.database import Base
from taskflow.repositories import TaskRepository, UserRepository, pwd_context
from taskflow.schemas import TaskCreate, TaskUpdate, UserCreate


@pytest.fixture()
def db() -> Session:
    """Create an in-memory SQLite database session for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def sample_user(db: Session) -> "UserCreate":
    """Return a sample UserCreate schema."""
    return UserCreate(
        username="johndoe",
        email="john@example.com",
        password="securepass123",
    )


@pytest.fixture()
def created_user(db: Session, sample_user: UserCreate):
    """Create and return a persisted user."""
    return UserRepository.create(db, sample_user)


@pytest.fixture()
def sample_task() -> TaskCreate:
    """Return a sample TaskCreate schema."""
    return TaskCreate(
        title="Test Task",
        description="A test task description",
        priority="high",
    )


@pytest.fixture()
def created_task(db: Session, created_user, sample_task: TaskCreate):
    """Create and return a persisted task."""
    return TaskRepository.create(db, sample_task, owner_id=created_user.id)


# --- UserRepository Tests ---


class TestUserRepositoryCreate:
    """Tests for UserRepository.create."""

    def test_should_create_user_with_hashed_password(
        self, db: Session, sample_user: UserCreate
    ) -> None:
        user = UserRepository.create(db, sample_user)
        assert user.id is not None
        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.hashed_password != "securepass123"
        assert pwd_context.verify("securepass123", user.hashed_password)

    def test_should_persist_user_in_database(
        self, db: Session, sample_user: UserCreate
    ) -> None:
        user = UserRepository.create(db, sample_user)
        fetched = db.get(type(user), user.id)
        assert fetched is not None
        assert fetched.username == "johndoe"


class TestUserRepositoryGetById:
    """Tests for UserRepository.get_by_id."""

    def test_should_return_user_by_id(self, db: Session, created_user) -> None:
        found = UserRepository.get_by_id(db, created_user.id)
        assert found is not None
        assert found.id == created_user.id
        assert found.username == created_user.username

    def test_should_return_none_for_nonexistent_id(self, db: Session) -> None:
        found = UserRepository.get_by_id(db, 9999)
        assert found is None


class TestUserRepositoryGetByUsername:
    """Tests for UserRepository.get_by_username."""

    def test_should_return_user_by_username(self, db: Session, created_user) -> None:
        found = UserRepository.get_by_username(db, "johndoe")
        assert found is not None
        assert found.id == created_user.id

    def test_should_return_none_for_nonexistent_username(self, db: Session) -> None:
        found = UserRepository.get_by_username(db, "nonexistent")
        assert found is None


class TestUserRepositoryVerifyPassword:
    """Tests for UserRepository.verify_password."""

    def test_should_verify_correct_password(
        self, db: Session, created_user
    ) -> None:
        assert UserRepository.verify_password(
            "securepass123", created_user.hashed_password
        )

    def test_should_reject_incorrect_password(
        self, db: Session, created_user
    ) -> None:
        assert not UserRepository.verify_password(
            "wrongpassword", created_user.hashed_password
        )


# --- TaskRepository Tests ---


class TestTaskRepositoryCreate:
    """Tests for TaskRepository.create."""

    def test_should_create_task_with_owner(
        self, db: Session, created_user, sample_task: TaskCreate
    ) -> None:
        task = TaskRepository.create(db, sample_task, owner_id=created_user.id)
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "A test task description"
        assert task.priority == "high"
        assert task.status == "todo"
        assert task.owner_id == created_user.id

    def test_should_set_default_status_to_todo(
        self, db: Session, created_user
    ) -> None:
        task = TaskRepository.create(
            db, TaskCreate(title="Simple"), owner_id=created_user.id
        )
        assert task.status == "todo"


class TestTaskRepositoryGetById:
    """Tests for TaskRepository.get_by_id."""

    def test_should_return_task_by_id(self, db: Session, created_task) -> None:
        found = TaskRepository.get_by_id(db, created_task.id)
        assert found is not None
        assert found.id == created_task.id
        assert found.title == "Test Task"

    def test_should_return_none_for_nonexistent_id(self, db: Session) -> None:
        found = TaskRepository.get_by_id(db, 9999)
        assert found is None


class TestTaskRepositoryListAll:
    """Tests for TaskRepository.list_all."""

    def test_should_return_all_tasks(
        self, db: Session, created_user
    ) -> None:
        for i in range(3):
            TaskRepository.create(
                db, TaskCreate(title=f"Task {i}"), owner_id=created_user.id
            )
        tasks = TaskRepository.list_all(db)
        assert len(tasks) == 3

    def test_should_support_pagination(
        self, db: Session, created_user
    ) -> None:
        for i in range(5):
            TaskRepository.create(
                db, TaskCreate(title=f"Task {i}"), owner_id=created_user.id
            )
        page = TaskRepository.list_all(db, skip=1, limit=2)
        assert len(page) == 2
        assert page[0].title == "Task 1"

    def test_should_return_empty_list_when_no_tasks(self, db: Session) -> None:
        tasks = TaskRepository.list_all(db)
        assert tasks == []


class TestTaskRepositoryListByOwner:
    """Tests for TaskRepository.list_by_owner."""

    def test_should_return_tasks_for_specific_owner(
        self, db: Session
    ) -> None:
        user1 = UserRepository.create(
            db, UserCreate(username="user1", email="u1@ex.com", password="password1234")
        )
        user2 = UserRepository.create(
            db, UserCreate(username="user2", email="u2@ex.com", password="password1234")
        )
        TaskRepository.create(db, TaskCreate(title="User1 Task"), owner_id=user1.id)
        TaskRepository.create(db, TaskCreate(title="User2 Task"), owner_id=user2.id)
        TaskRepository.create(db, TaskCreate(title="User1 Task 2"), owner_id=user1.id)

        user1_tasks = TaskRepository.list_by_owner(db, user1.id)
        assert len(user1_tasks) == 2
        assert all(t.owner_id == user1.id for t in user1_tasks)

        user2_tasks = TaskRepository.list_by_owner(db, user2.id)
        assert len(user2_tasks) == 1


class TestTaskRepositoryUpdate:
    """Tests for TaskRepository.update."""

    def test_should_update_task_title(self, db: Session, created_task) -> None:
        updated = TaskRepository.update(
            db, created_task.id, TaskUpdate(title="Updated Title")
        )
        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.description == "A test task description"  # unchanged

    def test_should_update_task_status(self, db: Session, created_task) -> None:
        updated = TaskRepository.update(
            db, created_task.id, TaskUpdate(status="done")
        )
        assert updated is not None
        assert updated.status == "done"

    def test_should_update_multiple_fields(self, db: Session, created_task) -> None:
        updated = TaskRepository.update(
            db,
            created_task.id,
            TaskUpdate(title="New", priority="low", status="in_progress"),
        )
        assert updated is not None
        assert updated.title == "New"
        assert updated.priority == "low"
        assert updated.status == "in_progress"

    def test_should_return_none_for_nonexistent_task(self, db: Session) -> None:
        result = TaskRepository.update(db, 9999, TaskUpdate(title="Nope"))
        assert result is None

    def test_should_not_change_unset_fields(self, db: Session, created_task) -> None:
        original_priority = created_task.priority
        updated = TaskRepository.update(
            db, created_task.id, TaskUpdate(title="Only Title Changed")
        )
        assert updated is not None
        assert updated.priority == original_priority


class TestTaskRepositoryDelete:
    """Tests for TaskRepository.delete."""

    def test_should_delete_existing_task(self, db: Session, created_task) -> None:
        task_id = created_task.id
        result = TaskRepository.delete(db, task_id)
        assert result is True
        assert TaskRepository.get_by_id(db, task_id) is None

    def test_should_return_false_for_nonexistent_task(self, db: Session) -> None:
        result = TaskRepository.delete(db, 9999)
        assert result is False
