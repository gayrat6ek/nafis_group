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

def getActiveProductWithDate(db:Session,product_id:UUID, active_from:datetime,active_to:datetime)->list[Discounts]:
    try:
        discounts = db.query(Discounts).join(DiscountProducts).filter(
            and_(
                Discounts.is_active == True,
                or_(
                    and_(
                        Discounts.active_from <= active_from,
                        Discounts.active_to >= active_from
                    ),
                    and_(
                        Discounts.active_from <= active_to,
                        Discounts.active_to >= active_to
                    ),
                    and_(
                        Discounts.active_from >= active_from,
                        Discounts.active_to <= active_to
                    )
                ),
                DiscountProducts.product_id == product_id
            )
        ).all()
        return discounts
    
    except SQLAlchemyError as e:
        raise e
    

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
            # products=[DiscountProducts(product_id=product_id) for product_id in data.product_ids] if data.product_ids else []
        )
        db.add(discount)
        db.commit()
        db.refresh(discount)

        for product_id in data.product_ids:
                if not getActiveProductWithDate(db=db,product_id=product_id,active_from=discount.active_from,active_to=discount.active_to):
                    discount_product = DiscountProducts(
                        discount_id=discount.id,
                        product_id=product_id
                    )
                    db.add(discount_product)
        return discount
    except SQLAlchemyError as e:
        db.rollback()
        raise False
    
def get_discounts(db: Session, is_active: Optional[bool] = None) -> list[Discounts]:
    try:
        query = db.query(Discounts)
        if is_active is not None:
            query = query.filter(Discounts.is_active == is_active).filter(
                
                    # and_(
                    #     Discounts.active_from <= datetime.now(tz=time_zone),
                    #     Discounts.active_to >= datetime.now(tz=time_zone)
                    # )
                
                 
            )
        query = query.order_by(Discounts.created_at.desc()).all()
        
        return query
        
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
        
        if data.name_uz is not None:
            discount.name_uz = data.name_uz
        if data.name_ru is not None:
            discount.name_ru = data.name_ru
        if data.name_en is not None:
            discount.name_en = data.name_en
        if data.description_uz is not None:
            discount.description_uz = data.description_uz
        if data.description_ru is not None:
            discount.description_ru = data.description_ru
        if data.description_en is not None:
            discount.description_en = data.description_en
        if data.is_news is not None:
            discount.is_news = data.is_news
        if data.is_active is not None:
            discount.is_active = data.is_active
        if data.amount is not None:
            discount.amount = data.amount
        if data.active_from is not None:
            discount.active_from = data.active_from
        if data.active_to is not None:
            discount.active_to = data.active_to
        if data.image is not None:  
            discount.image = data.image  # Assuming image is a URL or path to the image
        if data.product_ids is not None:
            # Clear existing products
            db.query(DiscountProducts).filter(DiscountProducts.discount_id == discount.id).delete()
            db.commit()
            
            # Add new products
            
            for product_id in data.product_ids:
                if not getActiveProductWithDate(db=db,product_id=product_id,active_from=discount.active_from,active_to=discount.active_to):
                    discount_product = DiscountProducts(
                        discount_id=discount.id,
                        product_id=product_id
                    )
                    db.add(discount_product)
            

        
        db.commit()
        db.refresh(discount)
        return discount
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

