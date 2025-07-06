

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
from app.crud import discounts as crud_discounts
from app.routes.depth import get_db, PermissionChecker

from app.schemas.discounts import DiscountGet, DiscountList, CreateDiscount, UpdateDiscount
from app.models.discounts import Discounts
from app.utils.permissions import pages_and_permissions

discounts_router = APIRouter()

@discounts_router.get('/discounts', response_model=List[DiscountList])
async def get_discount_list(
        is_active: bool = True,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Discounts']['view']))
):
    discounts = crud_discounts.get_discounts(db=db, is_active=is_active)
    return discounts


@discounts_router.get('/discounts/{id}', response_model=DiscountGet)
async def get_discount(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Discounts']['view']))
):
    discount = crud_discounts.get_discount_by_id(db=db, discount_id=id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@discounts_router.post('/discounts', response_model=DiscountGet)
async def create_discount(
        body: CreateDiscount,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Discounts']['create']))
):
    created_discount = crud_discounts.create_discount(db=db, data=body)
    return created_discount


@discounts_router.put('/discounts/{id}', response_model=DiscountGet)
async def update_discount(
        id: UUID,
        body: UpdateDiscount,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Discounts']['update']))
):
    discount = crud_discounts.get_discount_by_id(db=db, discount_id=id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    
    updated_discount = crud_discounts.update_discount(db=db, data=body, discount_id=id)
    return updated_discount