from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

# Rationale:
# - Pydantic v2 uses `model_config` for config, and `from_attributes=True` is needed for ORM mode.
# - Avoid redundant field redefinitions in subclasses unless you want to override defaults.
# - Consistent field ordering and typing for clarity.

class DeviceBase(BaseModel):
    name: str
    serial_number: str
    model: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    # All fields optional for PATCH-like update
    name: Optional[str] = None
    serial_number: Optional[str] = None
    model: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DeviceInDB(DeviceBase):
    id: UUID

class Device(DeviceInDB):
    pass
