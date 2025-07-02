
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud import districts as crud_districts
from app.routes.depth import get_db, PermissionChecker
from app.schemas.districts import DistrictGet, DistrictsList, CreateDistrict, UpdateDistrict
from app.models.districts import Districts
from app.utils.permissions import pages_and_permissions



districts_router = APIRouter()



@districts_router.get('/districts',)
async def get_district_list(
        page: int = 1,
        size: int = 10,
        is_active: bool = None,
        region_id: UUID = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Districts']['view']))
):
    return crud_districts.get_districts(db=db, page=page, size=size, region_id=region_id, is_active=is_active)


@districts_router.get('/districts/{id}', response_model=DistrictGet)
async def get_district(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Districts']['view']))
):
    district = crud_districts.get_district_by_id(db=db, district_id=id)
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district


@districts_router.post('/districts', response_model=DistrictGet)
async def create_district(
        body: CreateDistrict,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Districts']['create']))
):
    created_district = crud_districts.create_district(db=db, data=body)
    return created_district


@districts_router.put('/districts/{id}', response_model=DistrictGet)
async def update_district(
        id: UUID,
        body: UpdateDistrict,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Districts']['update']))
):
    districts = crud_districts.update_district(db=db, district_id=id, data=body)
    return districts
