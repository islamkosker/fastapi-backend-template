from os import name
from typing import Any, Dict, Optional, Union, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.sql import Device 
from app.crud.sql.base import CRUDBase 
from app.schemas.sql import DeviceCreate, DeviceUpdate
from sqlalchemy.future import select



class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    pass

        

device = CRUDDevice(Device)