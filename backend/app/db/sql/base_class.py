#app/db/sql/base_class.py

from datetime import datetime, timezone
from typing import Any, ClassVar, Optional
from sqlalchemy import UUID, Column, DateTime, Index, MetaData, text
from sqlalchemy.orm import as_declarative, declared_attr
import sqlalchemy.orm
import re


def camel_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

@as_declarative()
class Base:
    metadata: MetaData
    __abstract__ = True 
    include_create_update_index: ClassVar[bool] = True
    id: Any

    @declared_attr  # type: ignore
    def created_at(cls):
        if getattr(cls, "include_timestamps", True):
            return Column(
                DateTime(timezone=True),
                server_default=text("timezone('UTC', now())")
            )
        return None

    @declared_attr # type: ignore
    def updated_at(cls):
        if getattr(cls, "include_timestamps", True):
            return Column(
                DateTime(timezone=True),
                server_default=text("timezone('UTC', now())"),
                onupdate=lambda: datetime.now(timezone.utc)
            )
        return None

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  
        return camel_to_snake(cls.__name__)  # type: ignore[attr-defined]

    def __repr__(self) -> str:
        cls = self.__class__
        fields = [
            f"{k}={getattr(self, k, None)!r}"
            for k in vars(cls)
            if not k.startswith("_") and not callable(getattr(cls, k))
        ]
        return f"<{cls.__name__}({', '.join(fields)})>"

