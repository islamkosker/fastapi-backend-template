#app/models/sql/device.py

from pydoc import describe
import uuid
from sqlalchemy import UUID, Boolean, Column, ForeignKey, String, DateTime, text
from sqlalchemy.orm import relationship

from app.db.sql.base_class import Base


class Device(Base):
    # Device properties

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    model = Column(String, index=True, nullable=True)
    serial_number = Column(String, index=True, nullable=False, unique=True)

