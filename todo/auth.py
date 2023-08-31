"""Token based auth"""
from datetime import datetime, timedelta
from functools import partial
from fastapi import HTTPException, status

from jose import JWTError, jwt
from pydantic import BaseModel
from todo.config import settings
from todo.models import get_user, User

SECRET_KEY = settings.security.SECRET_KEY
ALGORITHM = settings.security.ALGORITHM


# Models 
class TokenData(BaseModel):
    user_name: str | None


# Functions
def create_access_token(data: dict, expires_delta: timedelta = None, scope: str = 'access_token') -> str:
    """Creates a JWT Token from user data"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire, 'scope': scope})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


create_refresh_token = partial(create_access_token, scope='refresh_token')


def get_current_user(token: str):
    """Get current user authenticated"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get('sub')
        if user_name is None:
            raise credentials_exception
        token_data = TokenData(user_name=user_name)
    except JWTError:
        raise credentials_exception
    user = get_user(user_name=token_data.user_name)
    if user is None:
        raise credentials_exception
    return user


def validate_token(token: str) -> User:
    """Validates user token"""
    user = get_current_user(token=token)
    return user
