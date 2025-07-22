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
from app.crud import productDetails as crud_product_details
from app.routes.depth import get_db, PermissionChecker
from app.schemas.productDetails import (
    ProductDetailsGet,
    ProductDetailsList,
    CreateProductDetails,
    UpdateProductDetails,
    CreateSize,
    UpdateSize
)

from app.models.productDetails import ProductDetails

from app.utils.permissions import pages_and_permissions
product_details_router = APIRouter()



@product_details_router.get('/product_details', response_model=List[ProductDetailsList])
async def get_product_details_list(
        product_id: UUID,
        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['view']))
):
    return crud_product_details.get_product_details(db=db, product_id=product_id, is_active=is_active)


@product_details_router.get('/product_details/{id}', response_model=ProductDetailsGet)
async def get_product_details(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['view']))
):
    product_detail = crud_product_details.get_product_details_by_id(db=db, product_detail_id=id)
    if not product_detail:
        raise HTTPException(status_code=404, detail="Product detail not found")
    return product_detail


@product_details_router.post('/product_details', response_model=ProductDetailsGet)
async def create_product_details(
        body: CreateProductDetails,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['create']))
):
    created_product_detail = crud_product_details.create_product_details(db=db, data=body)
    return created_product_detail



@product_details_router.put('/product_details/{id}', response_model=ProductDetailsGet)
async def update_product_details(
        id: UUID,
        body: UpdateProductDetails,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['update']))
):
    updated_product_detail = crud_product_details.update_product_details(db=db, data=body, product_detail_id=id)
    if not updated_product_detail:
        raise HTTPException(status_code=404, detail="Product detail not found")
    return updated_product_detail


@product_details_router.delete('/product/size/{id}')
async def delete_product_size(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['delete']))
):
    try:
        size = crud_product_details.delete_size(db=db, size_id=id)
        
        return {"detail": "Size deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@product_details_router.post('/product/size', response_model=ProductDetailsGet)
async def add_product_size(
        body: CreateSize,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['create']))
):
    try:
        created_size = crud_product_details.product_size_add(db=db, data=body)
        if not created_size:
            raise HTTPException(status_code=400, detail="Failed to add size")
        
        return {"detail": "Size added successfully", "size": created_size}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@product_details_router.put('/product/size/{id}', response_model=ProductDetailsGet)
async def update_product_size(
        id: UUID,
        body: UpdateSize,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['ProductDetails']['update']))
):
    try:
        updated_size = crud_product_details.update_size(db=db, size_id=id, data=body)
        if not updated_size:
            raise HTTPException(status_code=404, detail="Size not found")
        
        return {"detail": "Size updated successfully", "size": updated_size}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

