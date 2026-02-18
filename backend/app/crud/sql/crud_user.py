import email
from os import name
from typing import Any, Dict, Optional, Union, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.sql import User 
from app.crud.sql.base import CRUDBase 
from app.schemas.sql import UserCreate, UserUpdate
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["hashed_password"] = get_password_hash(obj_in_data.pop("password"))

        db_user = self.model(**obj_in_data) 
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
user = CRUDUser(User)