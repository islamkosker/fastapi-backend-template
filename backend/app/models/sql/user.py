# app/models/sql/user.py

import uuid
from sqlalchemy import UUID, Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.sql.base_class import Base


class User(Base):
    # User properties

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, index=True, nullable=False, unique=True)
    full_name = Column(String, index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False, index=True)

