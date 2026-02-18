from fastapi.security import (
    APIKeyHeader,
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from fastapi import Depends, HTTPException, status, Security
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.models.sql import User
from app.core import security
from jose import jwt


from app.db.sql.session import SessionLocal
from app.core.config import settings
from app.schemas.sql import TokenPayload

from typing import Any, Callable, Generator, Annotated, Type

from app.crud.sql.base import CRUDBase


reusable_oauth2_v1 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2_v1)]


def get_current_user(session: SessionDep, token: TokenDep) -> User: 
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not getattr(user, "is_active", False):
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_superuser(session: SessionDep, token: TokenDep) -> User:  # type: ignore
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not getattr(user, "is_active", False):
        raise HTTPException(status_code=404, detail="User not found")
    if not getattr(user, "is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges"
        )
    return user
