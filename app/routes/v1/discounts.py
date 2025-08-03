

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
from app.crud.loanMonths import get_loan_months
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
    loan_months = get_loan_months(db=db,is_active=True,limit=1)  # Ensure loan months are loaded if needed
    discounts = crud_discounts.get_discounts(db=db, is_active=is_active)
    for discount in discounts: 
        for product in discount.products:
            if product.product.details:
                for detail in product.product.details:
                    for size in detail.size:
                        if size.price and discount.amount:
                            cut_percent = size.price / 100 * discount.amount
                            size.curr_discount_price = size.price - cut_percent
                            size.discount = discount.amount
                        else:
                            size.curr_discount_price = None
                            size.discount = None
                        loan_month_prise = []
                        for month in loan_months:
                            if size.curr_discount_price:
                                extra_percent = (size.curr_discount_price / 100) * month.percent
                                total_price = size.curr_discount_price + extra_percent
                            else:
                                extra_percent = (size.price / 100) * month.percent
                                total_price = size.price + extra_percent
                            loan_month_prise.append({
                                "month": month.months,
                                "total_price": total_price,
                                "percent": month.percent
                            })
                        size.loan_months = loan_month_prise

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
    loan_months = get_loan_months(db=db,is_active=True,limit=1)  # Ensure loan months are loaded if needed
    for product in discount.products:
        if product.product.details:
            for detail in product.product.details:
                for size in detail.size:
                    if size.price and discount.amount:
                        cut_percent = size.price / 100 * discount.amount
                        size.curr_discount_price = size.price - cut_percent
                        size.discount = discount.amount
                    else:
                        size.curr_discount_price = None
                        size.discount = None
                    loan_month_prise = []
                    for month in loan_months:
                        if size.curr_discount_price:
                            extra_percent = (size.curr_discount_price / 100) * month.percent
                            total_price = size.curr_discount_price + extra_percent
                        else:
                            extra_percent = (size.price / 100) * month.percent
                            total_price = size.price + extra_percent

                        loan_month_prise.append({
                            "month": month.months,
                            "total_price": total_price,
                            "percent": month.percent
                        })
                    size.loan_months = loan_month_prise
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