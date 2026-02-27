"""Authentication router for TaskFlow API."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth import create_access_token, hash_password, verify_password
from .database import get_db
from .db_models import UserModel
from .schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserModel:
    """Register a new user account.

    Creates a user with a hashed password and returns the user profile.

    Raises:
        HTTPException: 400 if username or email already exists.
    """
    existing = db.query(UserModel).filter(
        (UserModel.username == user_data.username) | (UserModel.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    """Authenticate a user and return a JWT access token.

    Accepts OAuth2-compatible form data (username + password).

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
