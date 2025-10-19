import base64
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
from app.crud.users import get_one_user
from app.routes.depth import get_db, PermissionChecker
from app.schemas.orders import (
    AddOrUpdateCartItem,
    CartItemsSelect,
    OrderResponse,
    OrdersFullGet,
    RemoveCartItem,
    ConfirmOrder,
    OrdersGet,
    UpdateOrder
    )
from app.core.config import settings
from app.schemas.products import (
    ProductList)
from app.schemas.orders import OrderFilter

from app.utils.permissions import pages_and_permissions
from app.crud.loanMonths import get_loan_months
from app.utils.utils import timezonetash
from app.crud.userLocations import user_location as user_location_crud
from app.crud.regions import get_region_by_name
from app.utils.utils import find_region
from app.crud.sitevisits import stats_visits
from app.crud import productDetails as product_details_crud
from app.crud.limit import get_limit


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

    product_detail = product_details_crud.get_product_details_by_id(db=db, product_detail_id=body.product_detail_id)
    if not product_detail:
        raise HTTPException(status_code=404, detail="Product detail not found")
    
    size = product_detail.size.price * body.quantity

    
    get_user = get_one_user(db=db, user_id=current_user['id'])
    if not get_user.limit_total:
        get_user.limit_total = get_user.limit_total
    else:
        limit = get_limit(db=db)
        get_user.limit_total = limit.limit
    cart_total = crud_orders.get_user_cart_sum(db=db, user_id=current_user['id'])
    if cart_total + size > limit.limit:
        raise HTTPException(status_code=400, detail="You have reached your limit")
    
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
    cart.item_ids = []
    db.commit()

    if not orderItem:
        raise HTTPException(status_code=404, detail="Product detail or size not found")
    items = 0
    for item in cart.items:
        items += 1
    return {"message": "Item added to cart successfully", "items_count":items, "id":orderItem.id}


    

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
        selected:Optional[bool] = False,
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

    cart_items = cart.item_ids
    if selected and cart_items:
        for i in range(len(cart.items)-1, -1, -1):
            if str(cart.items[i].id) not in cart_items:
                del cart.items[i]
    
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
    total_items_price = sum(item.size.price * item.quantity for item in cart.items)  # original total
    total_price = sum(item.price * item.quantity for item in cart.items)  # discounted total
    total_discounted_price = total_items_price - total_price+cart.delivery_fee if cart.delivery_fee is None else total_items_price - total_price

    cart.items_count = item_count
    cart.total_items_price = total_items_price
    cart.total_discounted_price = total_discounted_price
    cart.total_amount = total_price



    return cart



@orders_router.post('/orders/confirm', response_model=OrderResponse)
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
    if order.payment_method =="payme":
        total_price = order.total_amount *100
        data = f"m={settings.payme_merchant_id};ac.order_id={order.id};a={total_price};c=https://nafis-home.uz/home/user/orders/active;ct=5"
        base_64_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        order.payment_url = f"https://checkout.paycom.uz/{base_64_data}"
    return order



@orders_router.get('/orders', response_model=Page[OrdersFullGet])
async def get_orders(
        
        filter: OrderFilter = Depends(),
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get a paginated list of orders for the user.
    """
    orders = crud_orders.get_orders(db=db, user_id=current_user['id'], page=filter.page, size=filter.size,filter=filter)
    return orders


@orders_router.get('/orders/{order_id}', response_model=OrdersFullGet)
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


@orders_router.get("/admin/orders", response_model=Page[OrdersFullGet])
async def get_all_orders(
        filter: OrderFilter = Depends(),
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['admin_view']))
):
    """
    Get a paginated list of all orders (admin view).
    """
    orders = crud_orders.get_orders(db=db, page=filter.page, size=filter.size, filter=filter)
    return orders



@orders_router.get('/admin/orders/{order_id}', response_model=OrdersFullGet)
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
    
    if body.loan_month_id:
        loan_month = crud_loanMonths.get_loan_months_by_id(db=db, loan_months_id=body.loan_month_id)
        if not loan_month:
            raise HTTPException(status_code=404, detail="Loan month not found")
    if body.user_location_id:
        user_location = user_location_crud.get(db, id=body.user_location_id)
        if not user_location:
            raise HTTPException(status_code=404, detail="User location not found")
        region = find_region(lat=user_location.latitude, lon=user_location.longitude)
        if not region:
            raise HTTPException(status_code=404, detail="Region not found for the given location")
        region_data = get_region_by_name(db=db, name=region['NAME_1'])

        if not region_data or not region_data.is_active:
            raise HTTPException(status_code=404, detail="Region is not active or not found")
        cart.delivery_fee = region_data.delivery_cost if region_data and region_data.delivery_cost is not None else 0.0
        cart.delivery_date = (
                datetime.now(timezonetash) + timedelta(days=region_data.delivery_days)
                if region_data and region_data.delivery_days is not None else None
            )
            
        
    else:
        cart.delivery_fee = 0.0

    
    cart = crud_orders.update_cart_items_selection(
        db=db,
        order_id=cart.id,
        item_ids=body.item_ids,
    )
    cart = crud_orders.get_cart_by_user_id(db=db, user_id=current_user['id'])
    
    total_items_price = 0
    total_discounted_price = 0
    total_price = 0
    item_count = 0
    for cart_item in cart.items:
        total_items_price += cart_item.size.price * cart_item.quantity
        total_discounted_price += (cart_item.size.price - cart_item.price) +cart.delivery_fee
        total_price += cart_item.price * cart_item.quantity
        item_count += 1
    
    cart.loan_month_price = (total_price+ cart.delivery_fee)*loan_month.percent/100 if body.loan_month_id else 0.0
    cart.total_amount = (total_price+ cart.delivery_fee)+cart.loan_month_price
    cart.loan_month_price = cart.total_amount/loan_month.months if body.loan_month_id else 0.0
    cart.loan_month_percent = loan_month.percent if body.loan_month_id else 0.0

    cart.items_count = item_count
    cart.total_items_price = total_items_price
    cart.total_discounted_price = total_discounted_price
    cart.loan_month_id = body.loan_month_id
    cart.pick_up_location_id = body.pick_up_location_id
    cart.user_location_id = body.user_location_id

    db.commit()
    
    if not cart:
        raise HTTPException(status_code=400, detail="Failed to update cart items selection")
    
    return {"message": "Cart items selection updated successfully"}


@orders_router.get('/purchased/products', response_model=Page[ProductList])
async def get_purchased_products(
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    """
    Get the list of products purchased by the current user.
    """
    products = crud_orders.get_purchased_product_list(db=db, user_id=current_user['id'], page=page, size=size)

    return products


@orders_router.put('/admin/orders/{order_id}')
async def update_order_status(
        order_id: UUID,
        data: UpdateOrder,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['admin_update_order']))
):
    """
    Update the status of a specific order (admin only).
    """
    order = crud_orders.get_order_by_id_admin(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    updated_order = crud_orders.updateOrderCrud(
        db=db,
        order_id=order_id,
        data=data
    )
    
    return {"success": True, "message": "Order status updated successfully", "order": updated_order}



@orders_router.get('/admin/statistics')
async def get_order_statistics(
        from_date:datetime,
        to_date:datetime,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['statistics']))
):
    """
    Get order statistics (admin only).
    """
    ravenue_stats= crud_orders.get_order_stats(db=db, from_date=from_date, to_date=to_date)
    order_status_breakdown= crud_orders.get_order_status_breakdown(db=db, from_date=from_date, to_date=to_date)
    by_region = crud_orders.get_region_stats(db=db, from_date=from_date, to_date=to_date)
    daily_visits = stats_visits(db=db, from_date=from_date,to_date=to_date)
    return {
        # ._mapping works on SQLAlchemy Row objects >=1.4
        "ravenue_stats": dict(ravenue_stats._mapping) if ravenue_stats else {},
        "order_status_breakdown": [dict(r._mapping) for r in order_status_breakdown],
        "by_region": [dict(r._mapping) for r in by_region],
        "daily_visits":[{"day": str(row.day), "visits": row.visits} for row in daily_visits]
    }
