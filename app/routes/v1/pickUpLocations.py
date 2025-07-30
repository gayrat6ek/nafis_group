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
from app.schemas.pickUpLocations import (
    PickUpLocationCreate,
    PickUpLocationUpdate,   
    PickUpLocationGet,
    PickUpLocationList
)
from app.crud import pickUpLocations as crud_pick_up_locations
from app.utils.permissions import pages_and_permissions


pick_up_locations_router = APIRouter()



@pick_up_locations_router.get('/pick_up_locations', response_model=List[PickUpLocationList])
async def get_pick_up_locations_list(
        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['PickUpLocations']['view']))
):
    return crud_pick_up_locations.getUpLocations(db=db, is_active=is_active)



@pick_up_locations_router.get('/pick_up_locations/{id}', response_model=PickUpLocationGet)
async def get_pick_up_location(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['PickUpLocations']['view']))
):
    pick_up_location = crud_pick_up_locations.getUpLocationById(db=db, location_id=id)
    if not pick_up_location:
        raise HTTPException(status_code=404, detail="Pick-up location not found")
    return pick_up_location



@pick_up_locations_router.post('/pick_up_locations', response_model=PickUpLocationGet)
async def create_pick_up_location(
        pick_up_location: PickUpLocationCreate,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['PickUpLocations']['create']))
):
    return crud_pick_up_locations.createUpLocations(db=db, data=pick_up_location)



@pick_up_locations_router.put('/pick_up_locations/{id}', response_model=PickUpLocationGet)
async def update_pick_up_location(
        id: UUID,
        pick_up_location: PickUpLocationUpdate,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['PickUpLocations']['update']))
):
    updated_location = crud_pick_up_locations.updateUpLocations(db=db, location_id=id, data=pick_up_location)
    if not updated_location:
        raise HTTPException(status_code=404, detail="Pick-up location not found")
    return updated_location





