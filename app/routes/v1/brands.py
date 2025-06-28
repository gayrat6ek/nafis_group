
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud import brands as crud_brands
from app.routes.depth import get_db, PermissionChecker
from app.schemas.brands import BrandGet, CreateBrand, UpdateBrand
from app.models.Brands import Brands
from app.utils.permissions import pages_and_permissions 


brands_router = APIRouter()

@brands_router.get('/brands', )
async def get_brand_list(
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Brands']['view']))
):
    return crud_brands.get_brands(db=db, page=page, size=size)



@brands_router.get('/brands/{brand_id}', response_model=BrandGet)
async def get_brand(
        brand_id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Brands']['view']))
):
    brand = crud_brands.get_brand_by_id(db=db, brand_id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@brands_router.post('/brands', response_model=BrandGet)
async def create_brand(
        brand: CreateBrand,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Brands']['create']))
):
    existing_brand = crud_brands.get_brand_by_name(db=db, name_uz=brand.name_uz)
    if existing_brand:
        raise HTTPException(status_code=400, detail="Brand with this name already exists")
    
    new_brand = crud_brands.create_brand(db=db, data=brand)
    return new_brand


@brands_router.put('/brands/{brand_id}', response_model=BrandGet)
async def update_brand(
        brand_id: UUID,
        brand: UpdateBrand,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Brands']['update']))
):
    existing_brand = crud_brands.get_brand_by_id(db=db, brand_id=brand_id)
    if not existing_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    updated_brand = crud_brands.update_brand(db=db, brand_id=brand_id, brand=brand)
    return updated_brand

