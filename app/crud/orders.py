

from pickletools import read_unicodestringnl
from re import L
from sqlalchemy.orm import contains_eager, aliased
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.orm import selectinload, with_loader_criteria
import bcrypt
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.models.ratings import Ratings
from app.utils.utils import timezonetash
from app.models.Orders import Orders
from app.models.OrderItems import OrderItems
from app.models.Products import Products
from app.models.productDetails import ProductDetails
from app.models.discountProducts import DiscountProducts
from app.models.reviews import Reviews
from app.models.discounts import Discounts
from app.crud import productDetails as product_details_crud
from app.schemas.orders import ConfirmOrder,OrderFilter, UpdateOrder
from app.crud.districts import get_district_by_id
from app.crud.discounts import activeDisCountProd
from app.crud.loanMonths import get_loan_months_by_id
from app.crud.regions import get_region_by_name
from app.utils.utils import find_region
from app.crud.userLocations import user_location as user_location_crud
from app.crud.orderPaymentDates import create_order_payment_date
from app.models.Users import Users
from app.crud.pickUpLocations import getUpLocationById

def get_cart_by_user_id(db: Session, user_id: UUID):
    try:
        now = datetime.now(timezonetash)


        query = (
            db.query(Orders).
            options(
                joinedload(Orders.items).
                joinedload(OrderItems.product_detail).
                joinedload(ProductDetails.product),
                with_loader_criteria(
                    DiscountProducts,
                    lambda dp: and_(
                        dp.discount.has(
                            and_(
                                Discounts.is_active == True,
                                Discounts.active_from <= now,
                                Discounts.active_to >= now
                            )
                        )
                    ),
                    include_aliases=True
                ),
            ).
            filter(
            Orders.user_id == user_id,
            Orders.status == 0  # Assuming 'cart' is the status for active carts
        ).first())
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
      

        if data.user_location_id:
            user_location = user_location_crud.get(db, id=data.user_location_id)
            region_find = find_region(lat=user_location.latitude, lon=user_location.longitude)
            if not region:
                raise HTTPException(status_code=404, detail="Region not found for the provided location")

            region = get_region_by_name(db, region_find['NAME_1'])
            if not region:
                raise HTTPException(status_code=404, detail="Region not found in the database")
            # delivery_cost = region.delivery_cost if region else 0.0
            delivery_cost = region.delivery_cost if region and region.delivery_cost is not None else 0.0
            delivery_date = (
                datetime.now(timezonetash) + timedelta(days=region.delivery_days)
                if region and region.delivery_days is not None else None
            )
            cart.region = region_find['NAME_1'] if region_find and 'NAME_1' in region_find else None
            cart.district = region_find['NAME_2'] if region_find and 'NAME_2' in region_find else None

            
        else:
            delivery_cost = 0.0
            delivery_date = None
            if data.pick_up_location_id is None:
                raise HTTPException(status_code=400, detail="Either user_location_id or pick_up_location_id must be provided for delivery.")
            pick_up_location = getUpLocationById(db, data.pick_up_location_id)

            cart.region = "ToshkentShahri"
            cart.district = pick_up_location.name_uz
            
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
        total_discounted_price = total_items_price - sum(item.price for item in cart.items) +delivery_cost
        total_price = sum(item.price * item.quantity for item in cart.items) 
        

        

        cart.items_count = item_count
        cart.total_items_price = total_items_price
        cart.total_discounted_price = total_discounted_price
        cart.loan_month_price = (total_price+ delivery_cost)*loan_month.percent/100 if data.loan_month_id else 0.0
        cart.total_amount = (total_price+ delivery_cost)+cart.loan_month_price
        cart.loan_month_price = cart.total_amount/loan_month.months if data.loan_month_id else 0.0
        
        cart.payment_method = data.payment_method
        cart.description = data.description
        cart.delivery_address = data.delivery_address
        cart.delivery_phone_number = data.delivery_phone_number
        cart.delivery_date = delivery_date
        cart.delivery_receiver = data.delivery_receiver
        cart.card_id = data.bank_card_id  # Assuming bank_card_id is the ID of the card used for payment
        cart.delivery_fee = delivery_cost
        cart.pick_up_location_id = data.pick_up_location_id
        cart.loan_month_id = data.loan_month_id
        cart.loan_month_percent = loan_month.percent if data.loan_month_id else 0.0
        cart.user_location_id = data.user_location_id  # Set the user's location ID for delivery, if applicable
        cart.created_at = datetime.now(timezonetash)

        # Update the cart status to 'confirmed' (assuming '1' is the status for confirmed orders)
        cart.status = 1

                

        db.commit()
        if cart.loan_month_id:
            create_order_payment_date(db=db,order_id=cart.id,months=loan_month.months,amount=cart.total_amount/loan_month.months)

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
    



def get_orders(db: Session, filter: OrderFilter, user_id: Optional[UUID] = None, page: int = 1, size: int = 10):
    try:
        # Base query for filtering and counting
        base_query = db.query(Orders).filter(Orders.status != 0)

        # If user_id is provided, filter only that user's orders
        if user_id is not None:
            base_query = base_query.filter(Orders.user_id == user_id)

        # Apply additional filters
        if filter.status is not None:
            base_query = base_query.filter(Orders.status == filter.status)
        if filter.is_paid is not None:
            base_query = base_query.filter(Orders.is_paid == filter.is_paid)
        if filter.filter == 'inactive':
            # Need to join to apply this filter if it's based on related tables
            base_query = base_query.filter(Orders.status.in_([5, 6]))
        elif filter.filter == 'active':
            base_query = base_query.filter(Orders.status.in_([1, 2, 3, 4]))
        elif filter.filter == 'loan':
            base_query = base_query.filter(Orders.loan_month_id.isnot(None))
        if filter.paymenttype is not None:
            base_query = base_query.filter(Orders.payment_method == filter.paymenttype.value)
        if filter.username:
            base_query = base_query.join(Users).filter(Users.full_name.ilike(f"%{filter.username}%"))
        if filter.created_at:
            base_query = base_query.filter(
                cast(Orders.created_at, Date) == filter.created_at
            )
        if filter.is_loan is not None:
            if filter.is_loan:
                base_query = base_query.filter(Orders.loan_month_id.isnot(None))
            else:
                base_query = base_query.filter(Orders.loan_month_id.is_(None))
        

        # --- Correctly count before adding complex joins for data fetching ---
        # The count query should only have joins necessary for the filters.
        # In this case, no extra joins are needed for the count.
        total_count = base_query.with_entities(func.count(Orders.id)).scalar()

        # --- Now build the main query to fetch data ---
        
        ReviewAlias = aliased(Reviews)
        
        query = (
            base_query
            .join(Orders.items)
            .join(OrderItems.product_detail)
            .join(ProductDetails.product)
            # This outerjoin is critical. It finds reviews ONLY if the user_id matches.
            # If no match is found, the review columns will be NULL.
            .outerjoin(
                ReviewAlias,
                and_(
                    Products.id == ReviewAlias.product_id,
                    Orders.user_id == ReviewAlias.user_id 
                )
            )
            # This tells SQLAlchemy to build the .reviews list from our specific outerjoin.
            # If the review columns were NULL, it will correctly create an empty list.
            .options(
                contains_eager(Orders.items)
                .contains_eager(OrderItems.product_detail)
                .contains_eager(ProductDetails.product)
                .contains_eager(Products.reviews, alias=ReviewAlias)
            )
            .distinct() # Add distinct to ensure each order is returned only once
        )


        # Apply ordering and pagination
        orders = query.order_by(Orders.created_at.desc()).offset((page - 1) * size).limit(size).all()

        # for order in orders:
        #     for item in order.items or []:
        #         product = item.product_detail.product if item.product_detail else None
        #         if product:
        #             for r in product.reviews or []:
        #                 print('all reviews',r.user_id, order.user_id)
        #             product.reviews = [r for r in (product.reviews or []) if r.user_id == order.user_id]
                    


        return {
            "items": orders,
            "total": total_count,
            "page": page,
            "size": size,
            "pages": (total_count + size - 1) // size if size > 0 else 0,
        }
    except SQLAlchemyError as e:
        # It's good practice to log the error here
        # import logging
        # logging.exception("Error fetching orders")
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
    

def getOrder(db: Session, id: UUID):
    try:
        order = db.query(Orders).filter(Orders.id == id).first()
        return order
    
    except SQLAlchemyError as e:
        raise e
    


def perform_transaction_orders(db:Session,order_id):
    try:
        query = db.query(Orders).filter(Orders.id==order_id).first()
        if query:
            query.is_paid = True
            db.commit()

        return query
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"internal server error")
    



def update_cart_items_selection(
        db: Session,
        order_id: UUID,
        item_ids: list[UUID]
):
    try:
        cart = db.query(Orders).filter(
            Orders.id == order_id,
            Orders.status == 0  # Ensure it's still a cart
        ).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        cart.item_ids = [str(item_id) for item_id in item_ids]
        
        db.commit()
        db.refresh(cart)
        return cart
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def get_purchased_product_list(db: Session, user_id: UUID, page: int = 1, size: int = 10):
    try:
        purchased_product_details = (
            db.query(ProductDetails.id)
            .join(OrderItems, ProductDetails.id == OrderItems.product_detail_id)
            .join(Orders, OrderItems.order_id == Orders.id)
            .filter(
                Orders.user_id == user_id,
                Orders.status.in_([1,2,3, 4, 5, 6])
                    )
                    .subquery()
                )

        products = (
            db.query(Products)
            .join(ProductDetails, Products.id == ProductDetails.product_id)
            .filter(ProductDetails.id.in_(purchased_product_details))
            .group_by(Products.id)
            .order_by(func.max(Orders.created_at).desc())
            .options(
                joinedload(Products.details.and_(
                    ProductDetails.id.in_(purchased_product_details)
                ))
            )
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return {
            "items": products,
            "total": len(products),
            "page": page,
            "size": size,
            'pages': (len(products) + size - 1) // size
        }


    except SQLAlchemyError as e:
        raise e
    


def updateOrderCrud(db:Session, order_id:UUID, data:UpdateOrder):
    try:
        order = db.query(Orders).filter(Orders.id==order_id).first()
        if not order:
            return None
        if data.status is not None:
            order.status = data.status
        if data.is_paid is not None:
            order.is_paid = data.is_paid
        if data.is_delivered is not None:
            order.is_delivered = data.is_delivered
        if data.description is not None:
            order.description = data.description
        if data.delivery_address is not None:
            order.delivery_address = data.delivery_address
        if data.delivery_phone_number is not None:
            order.delivery_phone_number = data.delivery_phone_number
        if data.delivery_receiver is not None:
            order.delivery_receiver = data.delivery_receiver
        if data.payment_method is not None:
            order.payment_method = data.payment_method
        if data.deny_reason is not None:
            order.deny_reason = data.deny_reason
        db.commit()
        db.refresh(order)
        return order
    except SQLAlchemyError as e:
        db.rollback()
        raise e