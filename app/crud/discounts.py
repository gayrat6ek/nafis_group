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

from app.models.discounts import Discounts
from app.models.productDetails import ProductDetails
from app.schemas.discounts import CreateDiscount, UpdateDiscount
from app.models.discountProducts import DiscountProducts
from app.models.Products import Products
import pytz

time_zone = pytz.timezone("Asia/Tashkent")



def create_discount(db: Session, data: CreateDiscount) -> Discounts:
    try:
        discount = Discounts(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            description_en=data.description_en,
            description_ru=data.description_ru,
            description_uz=data.description_uz,
            is_news=data.is_news,  # Assuming this is a flag for news or special discounts
            is_active=data.is_active,
            amount=data.amount,
            image=data.image,  # Assuming image is a URL or path to the image
            active_from=data.active_from,
            active_to=data.active_to,
            products=[DiscountProducts(product_id=product_id) for product_id in data.product_ids] if data.product_ids else []
        )
        db.add(discount)
        db.commit()
        db.refresh(discount)
        return discount
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
def get_discounts(db: Session, is_active: Optional[bool] = None) -> list[Discounts]:
    try:
        query = db.query(Discounts)
        if is_active is not None:
            query = query.filter(Discounts.is_active == is_active)
        
        return query.all()
        
    except SQLAlchemyError as e:
        raise e
    

def get_discount_by_id(db: Session, discount_id: UUID) -> Optional[Discounts]:
    try:
        return db.query(Discounts).filter(Discounts.id == discount_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_discount(db: Session, discount_id: UUID, data: UpdateDiscount) -> Optional[Discounts]:
    try:
        discount = db.query(Discounts).filter(Discounts.id == discount_id).first()
        if not discount:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            if key == "products":
                # Handle products separately
                if value is not None:
                    # Clear existing products
                    discount.products.clear()
                    # Add new products
                    for product_id in value:
                        discount.products.append(DiscountProducts(product_id=product_id))
            else:
                # Set other attributes directly 
                setattr(discount, key, value)

        
        db.commit()
        db.refresh(discount)
        return discount
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def activeDisCountProd(db: Session, product_id: UUID) -> list[Discounts]:
    try:
        discounts = db.query(Discounts).join(DiscountProducts).filter(
            and_(
                Discounts.is_active == True,
                Discounts.active_from <= datetime.now(tz=time_zone),
                Discounts.active_to >= datetime.now(tz=time_zone),
                DiscountProducts.product_id == product_id
            )
        ).all()
        return discounts
    
    except SQLAlchemyError as e:
        raise e 
    