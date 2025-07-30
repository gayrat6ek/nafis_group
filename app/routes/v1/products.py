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
                        size.curr_discount_price = size.price / (1 + product.discounts[0].discount.amount / 100)
                    else:
                        size.curr_discount_price = size.price
                    loan_month_prise = []
                    for month in loan_months:
                        extra_percent = (size.price /100)*month.precent
                        loan_month_prise.append({
                                "month": month.months,
                                "id": month.id,
                                "total_price": size.price*extra_percent/month.months,
                                "monthly_payment": size.price + extra_percent

                        })
                    size.loan_months = loan_month_prise
                        
    return products 



@products_router.get('/products/{id}', response_model=ProductGet)
async def get_product(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Products']['view']))
):
    product = crud_products.get_product_by_id(db=db, product_id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
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