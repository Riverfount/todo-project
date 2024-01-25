from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator
from slugify import slugify
from sqlmodel import Field, Session, SQLModel, select

from todo.db import engine
from todo.security import HashedPassword


class User(SQLModel, table=True):
    """Represents the User Model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=True)
    email: str = Field(nullable=True, unique=True)
    password: HashedPassword
    user_name: str = Field(nullable=False, unique=True)
    active: Optional[bool] = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    super_user: Optional[bool] = Field(default=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={'onupdate': datetime.utcnow}
    )


def gen_user_name(name: str) -> str:
    """Generates a slug user-name from a name"""
    return slugify(name)


class UserResponse(BaseModel):
    """Serializer for Get All User Response."""
    name: str
    user_name: str


class UserDetailResponse(UserResponse):
    """Serializer for User Detail Response."""
    active: bool
    super_user: bool
    created_at: datetime
    updated_at: datetime


class UserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_name: Optional[str] = None
    super_user: Optional[bool] = False

    @root_validator(pre=True)
    def generate_user_name_if_not_set(cls, values):
        """Generates username if not send."""
        if not values.get('user_name'):
            values['user_name'] = gen_user_name(values['name'])
        return values


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    super_user: Optional[bool] = False


def get_user(user_name: str = None) -> User | list[User] | None:
    query = (
        select(User).where(User.user_name == user_name).where(User.active) if user_name
        else select(User).where(User.active)
    )
    with Session(engine) as session:
        users = session.exec(query).first() if user_name else session.exec(query).all()
    return users
