"""Database connection"""

from sqlmodel import create_engine
from todo.config import settings

engine = create_engine(
    settings.db.uri,
    echo=False,
    connect_args=settings.db.connect_args
)
