from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from todo.auth import AuthenticatedUser, SuperUser
from todo.db import ActiveSession
from todo.models import (
    User,
    UserDetailResponse,
    UserRequest,
    UserResponse,
    get_user
)

router = APIRouter()


@router.get('/', response_model=list[UserResponse], dependencies=[AuthenticatedUser])
async def list_users():
    """List all users."""
    users = get_user()
    return users


@router.get('/{user_name}/', response_model=UserDetailResponse, dependencies=[AuthenticatedUser])
async def get_user_by_user_name(*, user_name: str):
    """Get user by user_name"""
    user = get_user(user_name=user_name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    return user


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[SuperUser])
async def create_user(*, user: UserRequest, session: Session = ActiveSession):
    """Creates new user"""
    db_user = User.from_orm(user)  # Transform UserRequest in User
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='E-mail or user-name already exists.')
    session.refresh(db_user)
    return db_user
