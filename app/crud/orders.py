

from pickletools import read_unicodestringnl
from re import L

from fastapi import HTTPException
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
from app.schemas.orders import ConfirmOrder
from app.crud.districts import get_district_by_id
from app.crud.discounts import activeDisCountProd
from app.crud.loanMonths import get_loan_months_by_id


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
        discount = activeDisCountProd(db, size.product_details.product_id)
        if discount:
            discounted_price = size.price/100* discount[0].amount
            size_price = size.price - discounted_price
        else:
            size_price = size.price

        if not size:
            raise ValueError("Size not found")
        
        order_item = db.query(OrderItems).filter(
            OrderItems.product_detail_id == product_detail_id,
            OrderItems.order_id == order_id,
            OrderItems.size_id == size_id  # Filter by size if applicable
        ).first()

        if order_item:
            # If the item already exists, update the quantity and price
            order_item.quantity = quantity
            order_item.price = size_price
        else:

            # If the item does not exist, create a new order item
            order_item = OrderItems(
                product_detail_id=product_detail_id,
                quantity=quantity,
                price=size_price,
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
    

def remove_item_from_cart(db: Session, id:UUID,order_id:UUID,):
    try:
        order_item = db.query(OrderItems).filter(
            OrderItems.id == id,
        )
        order_item = order_item.first()
        if not order_item:
            return None  # Item not found in the cart
        
        db.delete(order_item)
        db.commit()
        return order_item
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def confirm_card(user_id: UUID, db: Session, data:ConfirmOrder):
    try:
        cart = db.query(Orders).filter(
            Orders.user_id == user_id,
            Orders.status == 0  # Assuming '0' is the status for an active cart
        ).first()


        if data.loan_month_id:
            loan_month = get_loan_months_by_id(db, data.loan_month_id)
            if not loan_month:
                raise HTTPException(status_code=404, detail="Loan month not found")
            if not loan_month.is_active:
                raise HTTPException(status_code=400, detail="Loan month is not active")
            loan_month_percent = loan_month.percent
        else:
            loan_month_percent = 1

        # new_cart = get_cart_by_user_id(db, user_id)

        # if not new_cart:
        #     new_cart = create_cart(db, user_id)
        new_cart = []
        for item in cart.items:
            if item.id not in data.item_ids:
                new_cart.append({
                    "product_detail_id": item.product_detail_id,
                    "size_id": item.size_id,
                    "quantity": item.quantity
                })
                db.delete(item)

                
        db.flush()
        db.refresh(cart)
        # db.refresh(cart)
        if not cart.items:
            raise HTTPException(
                status_code=400,
                detail="Cart is empty. Please add items to the cart before confirming."
            )

        
        item_count = len(cart.items)
        total_items_price = sum(item.size.price * item.quantity for item in cart.items)
        total_discounted_price = total_items_price - sum(item.price for item in cart.items)
        total_price = sum(item.price * item.quantity for item in cart.items) 
        


        if data.district_id is not None:
            district = get_district_by_id(db, data.district_id)
            if not district:
                raise ValueError("District not found")
            if not district.region.delivery_cost:
                delivery_cost = 0.0
            else:
                delivery_cost = district.region.delivery_cost
        else:
            delivery_cost = 0.0

        cart.items_count = item_count
        cart.total_items_price = total_items_price
        cart.total_discounted_price = total_discounted_price
        cart.loan_month_price = (total_price+ delivery_cost)*loan_month_percent/100
        cart.total_amount = (total_price+ delivery_cost)+cart.loan_month_price
        
        cart.payment_method = data.payment_method
        cart.district_id = data.district_id
        cart.description = data.description
        cart.delivery_address = data.delivery_address
        cart.delivery_phone_number = data.delivery_phone_number
        cart.delivery_date = data.delivery_date
        cart.delivery_receiver = data.delivery_receiver
        cart.card_id = data.bank_card_id  # Assuming bank_card_id is the ID of the card used for payment
        cart.delivery_fee = delivery_cost
        cart.pick_up_location_id = data.pick_up_location_id
        cart.loan_month_id = data.loan_month_id
        cart.loan_month_percent = loan_month_percent

        # Update the cart status to 'confirmed' (assuming '1' is the status for confirmed orders)
        cart.status = 1

                

        db.commit()
        nextCard = get_cart_by_user_id(db, user_id)
        if not nextCard:
            # If the cart was empty, create a new cart
            nextCard = create_cart(db, user_id)
        for nItem in new_cart:
            add_or_update_item_cart(
                db=db,
                product_detail_id=nItem['product_detail_id'],
                quantity=nItem['quantity'],
                order_id=nextCard.id,
                size_id=nItem['size_id']
            )

        db.refresh(cart)
        return cart     
        
    except SQLAlchemyError as e:
        db.rollback()
        raise e 
    



def get_orders(db: Session, user_id: Optional[UUID]=None, page: int = 1, size: int = 10):
    try:
        query = db.query(Orders).filter(
            Orders.status != 0  # Exclude carts
        )
        if user_id:
            query = query.filter(Orders.user_id == user_id)

        total_count = query.count()
        query = query.order_by(Orders.created_at.desc()) 
        orders = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": orders,
            "total": total_count,
            "page": page,
            "size": size,
            'pages': (total_count + size - 1) // size 
        }
    except SQLAlchemyError as e:
        raise e
    


def get_order_by_id(db: Session, order_id: UUID) -> Optional[Orders]:
    try:
        order = db.query(Orders).filter(Orders.id == order_id).first()
        return order
    
    except SQLAlchemyError as e:
        raise e
    



def get_order_by_id_admin(db: Session, order_id: UUID) -> Optional[Orders]:
    try:
        return db.query(Orders).filter(Orders.id == order_id).first()
    
    except SQLAlchemyError as e:
        raise e