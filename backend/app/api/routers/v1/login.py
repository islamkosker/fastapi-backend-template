from typing import Annotated, Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

from app import crud, schemas, models
from app import dependencies
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter()


@router.post("/access-token")
def login_access_token(
    session: dependencies.SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schemas.sql.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        user = crud.sql.user.read_by_column(db=session, column=models.sql.User.email, value=form_data.username)

        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not bool(user.is_active):
            raise HTTPException(status_code=400, detail="Inactive User")
        if not verify_password(form_data.password, str(user.hashed_password)):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return schemas.sql.Token(access_token=create_access_token(user.id, expires_delta=access_token_expires))
    except Exception as e:
        # Convert the exception to a string to make it JSON serializable
        raise HTTPException(status_code=500, detail=str(e))

