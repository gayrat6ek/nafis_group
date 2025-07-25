

from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.models.Orders import Orders
from app.models.OrderItems import OrderItems
from app.crud import productDetails as product_details_crud


def get_cart_by_user_id(db: Session, user_id: UUID):
    try:
        query = db.query(Orders).filter(
            Orders.user_id == user_id,
            Orders.status == 0  # Assuming 'cart' is the status for active carts
        ).first()
        return query
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def create_cart(db: Session, user_id:UUID):
    try:
        cart = Orders(
            user_id=user_id,
            status=0,  # Assuming '0' is the status for an active cart
            total_amount=0.0,  # Initial amount is zero
            items_count=0,  # No items initially
            total_items_price=0.0,  # No items price initially
            total_discounted_price=0.0,  # No discounts initially
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart
    except SQLAlchemyError as e:
        db.rollback()
        raise e







def add_or_update_item_cart(db: Session, 
                     product_detail_id: UUID, 
                     quantity: int, 
                     order_id:UUID,
                     size_id:UUID
                     
                     ):
    try:
        size = product_details_crud.get_size_by_id(db, size_id)
        if not size:
            raise ValueError("Size not found")
        
        order_item = db.query(OrderItems).filter(
            OrderItems.product_detail_id == product_detail_id,
            OrderItems.order_id == order_id,
            OrderItems.size_id == size_id  # Filter by size if applicable
        ).first()

        if order_item:
            # If the item already exists, update the quantity and price
            order_item.quantity += quantity
            order_item.price = size.price
        else:

            # If the item does not exist, create a new order item
            order_item = OrderItems(
                product_detail_id=product_detail_id,
                quantity=quantity,
                price=size.price,
                order_id=order_id,
                size_id=size_id  # Set the size ID
            )
            db.add(order_item)  
        db.commit()
        db.refresh(order_item)
        return order_item
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def remove_item_from_cart(db: Session, order_item_id: UUID,order_id:UUID):
    try:
        order_item = db.query(OrderItems).filter(
            OrderItems.product_detail_id == order_item_id,
            OrderItems.order_id == order_id
        ).first()
        
        if not order_item:
            return None  # Item not found in the cart
        
        db.delete(order_item)
        db.commit()
        return order_item
    except SQLAlchemyError as e:
        db.rollback()
        raise e