from math import e
from multiprocessing import Value
from shutil import ExecError
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import TypeAdapter
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app import crud, schemas, models
from app import dependencies

router = APIRouter()


@router.post("/", response_model=schemas.sql.Device, status_code=201)
def create_device(
    *,
    db: Session = Depends(dependencies.get_db),
    current_user = Depends(dependencies.get_current_user),
    device_in: schemas.sql.DeviceCreate,
):
    existing_device = crud.sql.device.read_by_column(db=db, column=models.sql.Device.serial_number, value=device_in.serial_number) # TODO: Fix This 

    if existing_device:
        raise HTTPException(
            status_code=400,
            detail=f"Device with serial number '{device_in.serial_number}' already exists"
        )
    try:
    # Create device and associate with current user
        new_device = crud.sql.device.create(
            db=db, 
            obj_in=device_in, 
        )
        return schemas.sql.Device.model_validate(new_device)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



@router.get("/", response_model=List[schemas.sql.Device])
def read_devices(
    *,
    db: Session = Depends(dependencies.get_db),
    current_user = Depends(dependencies.get_current_user),
    offset = 0,
    limit = 100
) -> Any:
    # Get devices for the current user 

    devices = crud.sql.device.read_multi(db=db,offset=offset, limit=limit)
    return TypeAdapter(List[schemas.sql.Device]).validate_python(devices)


@router.get("/{device_id}", response_model=schemas.sql.Device)
def read_device(
    *,
    db: Session = Depends(dependencies.get_db),
    device_id: UUID,
    current_user = Depends(dependencies.get_current_user),
) -> Any:
    device = crud.sql.device.read(db=db, id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return schemas.sql.Device.model_validate(device)





