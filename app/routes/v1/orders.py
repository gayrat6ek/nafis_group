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
from app.crud import orders as crud_orders
from app.routes.depth import get_db, PermissionChecker
from app.schemas.orders import (
    AddOrUpdateCartItem,
    RemoveCartItem,
    ConfirmOrder,
    OrdersGet
    )

from app.utils.permissions import pages_and_permissions


orders_router = APIRouter()
@orders_router.post('/orders/cart/add', response_model=None)
async def add_to_cart(
        body: AddOrUpdateCartItem,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['create']))
):
    """
    Add an item to the user's cart.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        cart = crud_orders.create_cart(db=db, user_id=current_user['id'])
    
    item = crud_orders.add_or_update_item_cart(
        db=db, 
        order_id=cart.id, 
        product_detail_id=body.product_detail_id, 
        size_id=body.size_id, 
        quantity=body.quantity
    )
    if not item:
        raise HTTPException(status_code=404, detail="Product detail or size not found")
    return {"message": "Item added to cart successfully", "item_id": item.id}


    

@orders_router.post('/orders/cart/remove', )
async def remove_from_cart(
        body: RemoveCartItem,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['delete']))
):
    """
    Remove an item from the user's cart.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    success = crud_orders.remove_item_from_cart(db=db, 
                                                order_item_id=body.product_detail_id,
                                                order_id=cart.id,
                                                size_id=body.size
                                                )
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    return {"message": "Item removed from cart successfully"}



@orders_router.get('/my/cart', response_model=OrdersGet)
async def get_my_cart(
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get the user's cart.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    return cart



@orders_router.post('/orders/confirm', response_model=OrdersGet)
async def confirm_order(
        body: ConfirmOrder,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['create']))
):
    """
    Confirm the user's order.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    order = crud_orders.confirm_card(
        db=db, 
        user_id=current_user['id'],
        data=body
    )
    
    if not order:
        raise HTTPException(status_code=400, detail="Order confirmation failed")
    return order
