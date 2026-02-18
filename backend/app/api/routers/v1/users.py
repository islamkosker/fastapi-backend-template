from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.core.config import settings
from app import dependencies
from app import utils

router = APIRouter()



@router.post("/", response_model=schemas.sql.User, status_code=201)
def create_user(
    *,
    db: Session = Depends(dependencies.get_db), 
    user_in: schemas.sql.UserCreate,
) -> Any:

    if crud.sql.user.read_by_column(db=db, column=models.sql.User.email, value=user_in.email):
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = crud.sql.user.create(db=db, obj_in=user_in)
    return schemas.sql.User.model_validate(new_user)



@router.get("/me", response_model=schemas.sql.User)
def read_me(
    *,
    db: Session = Depends(dependencies.get_db),
    current_user=Depends(dependencies.get_current_user),
) -> Any:
    me = crud.sql.user.read(db=db, id=current_user.id)
    return schemas.sql.User.model_validate(me)


@router.get("/read_multi", response_model=List[schemas.sql.User])
def read_multi(
    *,
    db: Session = Depends(dependencies.get_db),
    superuser = Depends(dependencies.get_current_superuser)
) -> Any:
    read_multi_user = crud.sql.user.read_multi(db=db)
    return TypeAdapter(List[schemas.sql.User]).validate_python(read_multi_user)
