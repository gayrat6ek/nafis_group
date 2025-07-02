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

from app.models.productDetails import ProductDetails
from app.schemas.productDetails import CreateProductDetails, UpdateProductDetails

def create_product_details(db: Session, data: CreateProductDetails) -> ProductDetails:
    try:
        product_details = ProductDetails(
            product_id=data.product_id,
            size=data.size,
            characteristics=data.characteristics,
            is_active=True,
            video_info=data.video_info,
            images=data.images,
            price=data.price,
            quantity=data.quantity,
            color_id=data.color_id,
        )
        db.add(product_details)
        db.commit()
        db.refresh(product_details)
        return product_details
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def get_product_details(db: Session, product_id: UUID, is_active: Optional[bool] = None) -> list[ProductDetails]:
    try:
        query = db.query(ProductDetails).filter(ProductDetails.product_id == product_id)
        if is_active is not None:
            query = query.filter(ProductDetails.is_active == is_active)
        
        return query.all()
        
    except SQLAlchemyError as e:
        raise e

def get_product_details_by_id(db: Session, product_details_id: UUID) -> Optional[ProductDetails]:
    try:
        return db.query(ProductDetails).filter(ProductDetails.id == product_details_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_product_details(db: Session, product_details_id: UUID, data: UpdateProductDetails) -> Optional[ProductDetails]:
    try:
        product_details = db.query(ProductDetails).filter(ProductDetails.id == product_details_id).first()
        if not product_details:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(product_details, key, value)
        
        db.commit()
        db.refresh(product_details)
        return product_details
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

