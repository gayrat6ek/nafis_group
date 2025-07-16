from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page
from sqlalchemy.orm import Session


from app.routes.depth import get_db, PermissionChecker
from app.crud import measureUnits as crud_measure_units
from app.schemas.measureUnits import (
    MeasureUnitsGet,
    MeasureUnitsList,
    CreateMeasureUnits,      
    UpdateMeasureUnits,
)
from app.models.measureUnits import MeasureUnits
from app.utils.permissions import pages_and_permissions 

measure_units_router = APIRouter()



@measure_units_router.get('/measure_units', response_model=List[MeasureUnitsList])
async def get_measure_units_list(
        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['MeasureUnits']['view']))
):
    return crud_measure_units.get_measure_units(db=db, is_active=is_active)


@measure_units_router.get('/measure_units/{id}', response_model=MeasureUnitsGet)
async def get_measure_unit( 
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['MeasureUnits']['view']))
):
    measure_unit = crud_measure_units.get_measure_unit_by_id(db=db, measure_unit_id=id)
    if not measure_unit:
        raise HTTPException(status_code=404, detail="Measure unit not found")
    return measure_unit


@measure_units_router.post('/measure_units', response_model=MeasureUnitsGet)
async def create_measure_unit(  
        body: CreateMeasureUnits,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['MeasureUnits']['create']))
):
    created_measure_unit = crud_measure_units.create_measure_unit(db=db, data=body)
    return created_measure_unit


@measure_units_router.put('/measure_units/{id}', response_model=MeasureUnitsGet)
async def update_measure_unit(
        id: UUID,
        body: UpdateMeasureUnits,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['MeasureUnits']['update']))
):
    updated_measure_unit = crud_measure_units.update_measure_unit(db=db, measure_unit_id=id, data=body)
    if not updated_measure_unit:
        raise HTTPException(status_code=404, detail="Measure unit not found")
    return updated_measure_unit

