from datetime import datetime, timedelta
from typing import List, Optional, Union
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
from app.crud import loanMonths as crud_loanMonths
from app.routes.depth import get_db, PermissionChecker
from app.schemas.orders import (
    AddOrUpdateCartItem,
    CartItemsSelect,
    RemoveCartItem,
    ConfirmOrder,
    OrdersGet
    )

from app.utils.permissions import pages_and_permissions
from app.crud.loanMonths import get_loan_months
from app.utils.utils import timezonetash

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
    
    orderItem = crud_orders.add_or_update_item_cart(
        db=db,
        order_id=cart.id,
        product_detail_id=body.product_detail_id, 
        size_id=body.size_id, 
        quantity=body.quantity
    )
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])

    # delivery_date = 0

    # for item in cart.items:
    #     if item.product_detail.product.delivery_days:
    #         delivery_date = max(delivery_date, item.product_detail.product.delivery_days)
    # cart.delivery_date = datetime.now(tz=timezonetash) + timedelta(days=delivery_date)


    item_count = len(cart.items)
    total_items_price = sum(item.size.price * item.quantity for item in cart.items)
    total_discounted_price = total_items_price - sum(item.price for item in cart.items)
    total_price = sum(item.price * item.quantity for item in cart.items)


    cart.items_count = item_count
    cart.total_items_price = total_items_price
    cart.total_discounted_price = total_discounted_price
    cart.total_amount = total_price
    db.commit()

    if not orderItem:
        raise HTTPException(status_code=404, detail="Product detail or size not found")
    items = 0
    for item in cart.items:
        items += 1
    return {"message": "Item added to cart successfully", "items_count":items, "id":orderItem.product_detail.product_id}


    

@orders_router.post('/orders/cart/remove', )
async def remove_from_cart(
        body: list[RemoveCartItem],
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['remove_from_cart']))
):
    """
    Remove an item from the user's cart.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    for item in body:
    
        success = crud_orders.remove_item_from_cart(db=db, 
                                                    id=item.item_id,
                                                    order_id=cart.id,
                                                    )

    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    item_count = len(cart.items)
    total_items_price = sum(item.size.price * item.quantity for item in cart.items)
    total_discounted_price = total_items_price - sum(item.price for item in cart.items)
    total_price = sum(item.price * item.quantity for item in cart.items)
    cart.items_count = item_count
    cart.total_items_price = total_items_price
    cart.total_discounted_price = total_discounted_price
    cart.total_amount = total_price
    db.commit()
    
    return {"message": "Item removed from cart successfully"}



@orders_router.get('/my/cart', response_model=Union[ dict,OrdersGet])
async def get_my_cart(
        get_len:Optional[bool] = False,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get the user's cart.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        return {"items_count": 0, "message": "Cart is empty"}
    if get_len:
        items_count = len(cart.items)
        return {"items_count": items_count}
    
    loan_month = get_loan_months(db=db, is_active=True,limit=1)
    
    for item in cart.items:
        if item.product_detail.product.discounts:
            cut_percent = item.size.price / 100 * item.product_detail.product.discounts[0].discount.amount
            item.size.curr_discount_price = item.size.price - cut_percent
            item.size.discount = item.product_detail.product.discounts[0].discount.amount
        else:
            item.size.curr_discount_price = None
            item.size.discount = None
        
        loan_month_prise = []
        for month in loan_month:
            if item.size.curr_discount_price:
                extra_percent = (item.size.curr_discount_price / 100) * month.percent
                total_price = item.size.curr_discount_price + extra_percent
            else:
                extra_percent = (item.size.price / 100) * month.percent
                total_price = item.size.price + extra_percent

            loan_month_prise.append({
                "month": month.months,
                "id": month.id,
                "total_price": total_price,
                "monthly_payment": total_price / month.months
            })
        item.size.loan_months = loan_month_prise

   

    item_count = len(cart.items)
    total_items_price = sum(item.size.price * item.quantity for item in cart.items)
    total_discounted_price = total_items_price - sum(item.price for item in cart.items)
    total_price = sum(item.price * item.quantity for item in cart.items)

    cart.items_count = item_count
    cart.total_items_price = total_items_price
    cart.total_discounted_price = total_discounted_price



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
        data=body,
    )
    
    if not order:
        raise HTTPException(status_code=400, detail="Order confirmation failed")
    return order



@orders_router.get('/orders', response_model=Page[OrdersGet])
async def get_orders(
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get a paginated list of orders for the user.
    """
    orders = crud_orders.get_orders(db=db, user_id=current_user['id'], page=page, size=size)
    return orders


@orders_router.get('/orders/{order_id}', response_model=OrdersGet)
async def get_order(
        order_id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get details of a specific order by its ID.
    """
    order = crud_orders.get_order_by_id(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@orders_router.get("/admin/orders", response_model=Page[OrdersGet])
async def get_all_orders(
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get a paginated list of all orders (admin view).
    """
    orders = crud_orders.get_orders(db=db, page=page, size=size)
    return orders



@orders_router.get('/admin/orders/{order_id}', response_model=OrdersGet)
async def get_order_by_id(
        order_id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get details of a specific order by its ID (admin view).
    """
    order = crud_orders.get_order_by_id_admin(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order



@orders_router.put('/cart/items/selection')
async def select_cart_items(
        body: CartItemsSelect,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['update']))
):
    """
    Select specific items in the user's cart.
    """
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    updated_cart = crud_orders.update_cart_items_selection(
        db=db,
        order_id=cart.id,
        item_ids=body.item_ids
    )
    
    if not updated_cart:
        raise HTTPException(status_code=400, detail="Failed to update cart items selection")
    
    return {"message": "Cart items selection updated successfully"}