"""
SQLAlchemy 2.0 CRUDBase Modernization Guide
===========================================

This module is designed for SQLAlchemy 2.0+ and uses the recommended modern patterns for ORM CRUD operations.

Key Changes and Best Practices for SQLAlchemy 2.0:
--------------------------------------------------
1. Querying:
   - Use `select(Model)` and `db.execute(stmt)` instead of `db.query(Model)`.
   - Use `.where(...)` on the select statement instead of `.filter(...)`.
   - Use `.scalars().first()` or `.scalars().all()` to retrieve ORM objects from results.

2. Results:
   - `.scalars().first()` returns the first result or None.
   - `.scalars().all()` returns all results as a Sequence (cast to `list()` for type safety).

3. Creating Objects:
   - Use `db.add(obj)`, `db.commit()`, and `db.refresh(obj)` as before.
   - Use `jsonable_encoder` to convert Pydantic models to dicts for ORM instantiation.

4. Updating Objects:
   - Use Pydantic v2's `.model_dump(exclude_unset=True)` or v1's `.dict(exclude_unset=True)` to get update data.
   - Set attributes directly on the ORM object, then commit and refresh.

5. Deleting Objects:
   - Use `db.get(Model, id)` to fetch by primary key, then `db.delete(obj)` and `db.commit()`.

6. Type Hints:
   - Use `List[ModelType]` for type hints (from `typing`), but always cast results to `list()` in code.

7. No `.query()` or legacy Query API:
   - All `.query()` usage is replaced by `select()` and `db.execute()`.

Reference: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html

Legacy (1.x)         | SQLAlchemy 2.0 Modern
---------------------|-----------------------------
db.query(Model)      | select(Model) + db.execute
.filter(...)         | .where(...)
.first(), .all()     | .scalars().first(), .scalars().all()
.query().offset().limit() | select().offset().limit()
"""

from dataclasses import field
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import GenerativeSelect
from sqlalchemy.orm import Mapper, Session, foreign
from sqlalchemy import Column
from sqlalchemy.future import select
from app.db.sql.base import Base
from sqlalchemy.inspection import inspect


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)



class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Create - Read - Update - Delete
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(
        self, db: Session, *, obj_in: CreateSchemaType, foreign_key: Optional[dict] = None
    ) -> ModelType:
        """
        Create a new record in the database, optionally merging extra fields like foreign keys.
        """
        obj_in_data = jsonable_encoder(obj_in)

        if foreign_key:
            obj_in_data.update(foreign_key)

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def read(self, db: Session, id: Union[UUID, int]) -> Optional[ModelType]:
        """
        Retrieve a single record by its unique identifier.

        Args:
            db (Session): The SQLAlchemy database session.
            id (UUID): The unique identifier of the record.

        Returns:
            Optional[ModelType]: The record if found, otherwise None.
        """
        stmt = select(self.model).where(self.model.id == id)
        return db.execute(stmt).scalar()



    def read_by_column(self, db: Session, column: Column, value: Any) -> Optional[ModelType]:
        """    
         Read a single record by a given model column and value.
        """
        if not hasattr(self.model, column.name) or getattr(self.model, column.name) is not column:
            raise ValueError(f"Column '{column.name}' does not belong to model '{self.model.__name__}'")
        
        stmt = select(self.model).where(column == value).limit(1)
        return db.execute(stmt).scalar_one_or_none()


    
    def read_multi_by_column(self, db: Session, column: Column, values: Any) -> List[ModelType]:
        """    
         Read multiple records by a given model column and a value or list of values.

         Args:
            db (Session): The SQLAlchemy database session.
            column (Column): The model column to filter by.
            values (Any): A single value or a list of values to match.

         Returns:
            List[ModelType]: A list of matching records.
        """
        if not hasattr(self.model, column.name) or getattr(self.model, column.name) is not column:
            raise ValueError(f"Column '{column.name}' does not belong to model '{self.model.__name__}'")
        
        
        stmt = select(self.model).where(column.in_(values))

        return list(db.execute(stmt).scalars().all())


    def read_multi(
        self, db: Session, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple records with optional pagination.

        Args:
            db (Session): The SQLAlchemy database session.
            offset (int, optional): The number of records to skip. Defaults to 0.
            limit (int, optional): The maximum number of records to return. Defaults to 0 (no limit).

        Returns:
            List[ModelType]: A list of records.
        """
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars().all())

  

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Update an existing database object with new values.

        This method supports only Pydantic v2 for schema updates. If `obj_in` is a Pydantic model, it uses
        `.model_dump(exclude_unset=True)` to extract only the fields that are set. If `obj_in` is a dict, it is used directly.
        Only fields present in the update data will be updated on the database object.

        Args:
            db (Session): The SQLAlchemy session.
            db_obj (ModelType): The existing ORM object to update.
            obj_in (UpdateSchemaType | dict): The update data, either as a Pydantic v2 model or a dict.

        Returns:
            ModelType: The updated ORM object.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: UUID) -> Optional[ModelType]:
        """
        Delete an object from the database by its primary key (UUID).

        If the object with the given ID does not exist, raises a ValueError.

        Args:
            db (Session): The SQLAlchemy session.
            id (UUID): The primary key of the object to delete.

        Returns:
            Optional[ModelType]: The deleted ORM object if found and deleted.

        Raises:
            ValueError: If the object with the given ID is not found.
        """
        obj = db.get(self.model, id)
        if obj is None:
            raise ValueError(f"{self.model.__name__} with id {id} not found")
        db.delete(obj)
        db.commit()
        return obj


