from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Represents the User Model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=True)
    email: str = Field(nullable=True, unique=True)
    password: str = Field(nullable=False)
    user_name: str = Field(nullable=False, unique=True)
    active: Optional[bool] = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={'onupdate': datetime.utcnow}
    )
