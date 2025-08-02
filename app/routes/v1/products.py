from typing import List, Optional
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
from app.crud import products as crud_products
from app.routes.depth import get_db, PermissionChecker
from app.schemas.products import (
    ProductGet,
    ProductList,
    CreateProduct,
    UpdateProduct,)
    
from app.crud.likes import is_liked


from app.models.Products import Products
from app.crud.loanMonths import get_loan_months
from app.utils.permissions import pages_and_permissions
products_router = APIRouter()



@products_router.get('/products', response_model=Page[ProductList])
async def get_products_list(
        page: int = 1,
        size: int = 10,
        category_id: Optional[UUID] = None,
        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Products']['view']))
):
    products = crud_products.get_products(db=db, page=page, size=size, is_active=is_active, category_id=category_id)
    #if  product has discounts then update add to detailsize product curr_discount_price discount in precentate
    loan_months = get_loan_months(db=db,is_active=True)  # Ensure loan months are loaded if needed
    for product in products['items']:
            for detail in product.details:
                for size in detail.size:
                    if size.price and product.discounts:
                        cut_percent = size.price/100 * product.discounts[0].discount.amount
                        size.curr_discount_price = size.price - cut_percent
                        size.discount = product.discounts[0].discount.amount
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
                            "id": month.id,
                            "total_price": total_price,
                            "monthly_payment": total_price / month.months
                        })
                    size.loan_months = loan_month_prise
                        
    return products 



@products_router.get('/products/{id}', response_model=ProductGet)
async def get_product(
        id: UUID,
        user_id: Optional[UUID] = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Products']['view']))
):
    product = crud_products.get_product_by_id(db=db, product_id=id)
    loan_months = get_loan_months(db=db,is_active=True)    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found") 
    if user_id is not None:
        product.liked = is_liked(db=db, user_id=user_id, product_id=id)



    for detail in product.details:
                for size in detail.size:
                    if size.price and product.discounts:
                        cut_percent = size.price/100 * product.discounts[0].discount.amount
                        size.curr_discount_price = size.price - cut_percent
                        size.discount = product.discounts[0].discount.amount
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
                            "id": month.id,
                            "total_price": total_price,
                            "monthly_payment": total_price / month.months
                        })
                    size.loan_months = loan_month_prise
    
    return product



@products_router.post('/products', response_model=ProductGet)
async def create_product(
        body: CreateProduct,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Products']['create']))
):
    created_product = crud_products.create_product(db=db, data=body)
    return created_product


@products_router.put('/products/{id}', response_model=ProductGet)
async def update_product(
        id: UUID,
        body: UpdateProduct,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Products']['update']))
):
    updated_product = crud_products.update_product(db=db, product_id=id, data=body)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product




@products_router.get('/liked/products', response_model=Page[ProductList])
async def get_liked_products(
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Products']['view']))
):
    """
    Get the list of products liked by the current user.
    """
    liked_products = crud_products.get_liked_products(db=db, user_id=current_user['id'], page=page, size=size)
    return liked_products