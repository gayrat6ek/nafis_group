from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload, with_loader_criteria
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.productDetails import ProductDetails
from app.schemas.productDetails import CreateProductDetails, UpdateProductDetails,CreateSize,UpdateSize
from app.models.sizes import Sizes

def create_product_details(db: Session, data: CreateProductDetails) -> ProductDetails:
    try:
        product_details = ProductDetails(
            product_id=data.product_id,
            # sizes=data.sizes,
            is_active=True,
            video_info=data.video_info,
            images=data.images,
            # price=data.price,
            quantity=data.quantity,
            color_id=data.color_id,
            measure_unit_id=data.measure_unit_id  # Assuming measure_unit_id is part of the CreateProductDetails schema
        )
        db.add(product_details)
        db.commit()
        for size in data.sizes:
            size_instance = Sizes(
                value=size['value'],  # Assuming size is a dictionary with a 'value' key
                price=size.get('price'),  # Optional price for the size
                detail_id=product_details.id  # Linking the size to the product detail
            )
            db.add(size_instance)
        db.commit()
        db.refresh(product_details)

        return product_details
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def get_product_details(db: Session, product_id: UUID, is_active: Optional[bool] = None) -> list[ProductDetails]:
    try:
        query = (
            db.query(ProductDetails)
            .filter(ProductDetails.product_id == product_id)
            .options(
                selectinload(ProductDetails.size),
                with_loader_criteria(Sizes, Sizes.is_deleted == False)
            )
)

        return query.all()
        
    except SQLAlchemyError as e:
        raise e

def get_product_details_by_id(db: Session, product_detail_id: UUID) -> Optional[ProductDetails]:
    try:
        return (db.query(ProductDetails).filter(ProductDetails.id == product_detail_id)
                .options(
                    selectinload(ProductDetails.size),
                    with_loader_criteria(Sizes, Sizes.is_deleted == False)
                    
                )
                .first()
                )
    except SQLAlchemyError as e:
        raise e
    

def update_product_details(db: Session, product_detail_id: UUID, data: UpdateProductDetails) -> Optional[ProductDetails]:
    try:
        product_details = db.query(ProductDetails).filter(ProductDetails.id == product_detail_id).first()
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
    

def delete_size(db: Session, size_id: UUID) -> Optional[Sizes]:
    try:
        size = db.query(Sizes).filter(Sizes.id == size_id).first()
        if not size:
            return None
        
        size.is_deleted = True  # Marking the size as deleted
        db.commit()
        return size
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def product_size_add(db: Session, data:CreateSize) -> Sizes:
    try:
        size = Sizes(
            value=data.value,
            price=data.price,
            detail_id=data.detail_id
        )
        db.add(size)
        db.commit()
        db.refresh(size)
        return size
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def update_size(db: Session, size_id: UUID, data: UpdateSize) -> Optional[Sizes]:
    try:
        size = db.query(Sizes).filter(Sizes.id == size_id).first()
        if not size:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(size, key, value)
        
        db.commit()
        db.refresh(size)
        return size
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_size_by_id(db: Session, size_id: UUID) -> Optional[Sizes]:
    try:
        return db.query(Sizes).filter(Sizes.id == size_id).first()
    except SQLAlchemyError as e:
        raise e

