from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from todo.db import ActiveSession
from todo.models import User, UserDetailResponse, UserRequest, UserResponse

router = APIRouter()


@router.get('/', response_model=list[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = session.exec(select(User)).all()
    return users


@router.get('/{user_name}/', response_model=UserDetailResponse)
async def get_usert_by_user_name(*, user_name: str, session: Session = ActiveSession):
    """Get user by user_name"""
    query = select(User).where(User.user_name == user_name)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    return user


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(*, user: UserRequest, session: Session = ActiveSession):
    """Creates new user"""
    # TODO: Validar informações recebidas com as constraints do banco.
    db_user = User.from_orm(user)  # Transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
