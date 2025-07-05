from uuid import UUID
from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud import regions as crud_regions
from app.routes.depth import get_db, PermissionChecker
from app.schemas.regions import  RegionGet,RegionsList,CreateRegion,UpdateRegion
from app.models.regions import Regions
from app.utils.permissions import pages_and_permissions



regions_router = APIRouter()


@regions_router.get('/regions')
async def get_region_list(
        page: int = 1,
        size: int = 10,
        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Regions']['view']))
):
    return crud_regions.get_regions(db=db, page=page, size=size, is_active=is_active)


@regions_router.get('/regions/{id}', response_model=RegionGet)
async def get_region(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Regions']['view']))
):
    region = crud_regions.get_region_by_id(db=db, region_id=id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


@regions_router.post('/regions', response_model=RegionGet)
async def create_region(
        body: CreateRegion,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Regions']['create']))
):
    created_region = crud_regions.create_region(db=db, data=body)
    return created_region



@regions_router.put('/regions/{id}', response_model=RegionGet)
async def update_region(
        id: UUID,
        body: UpdateRegion,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Regions']['update']))
):
    region = crud_regions.get_region_by_id(db=db, region_id=id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    updated_region = update_region(db=db, region_id=id, data=body)
    return updated_region







