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
        if data.size:
            for size in data.size:
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
        query = query.order_by(ProductDetails.created_at.desc())
        if is_active is not None:
            query = query.filter(ProductDetails.is_active == is_active)

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
        if data.is_active is not None:
            product_details.is_active = data.is_active
        if data.video_info is not None:
            product_details.video_info = data.video_info
        if data.images is not None:
            product_details.images = data.images 
        if data.quantity is not None:
            product_details.quantity = data.quantity
        if data.color_id is not None:
            product_details.color_id = data.color_id
        if data.measure_unit_id is not None:
            product_details.measure_unit_id = data.measure_unit_id  # Assuming measure_unit_id is part of the UpdateProductDetails schema   



        
        db.commit()
        db.refresh(product_details)

        # Update sizes if provided and if size inside of detail is not in data.sizes the delete =True

        if data.size:
            # Step 1: Get all current sizes from DB for this detail
            existing_sizes = db.query(Sizes).filter(Sizes.detail_id == product_detail_id, Sizes.is_deleted == False).all()

            # Step 2: Track incoming size values
            incoming_values = set(size_data.value for size_data in data.size)

            # Step 3: Soft-delete sizes that are not in incoming data
            for existing_size in existing_sizes:
                if existing_size.value not in incoming_values:
                    existing_size.is_deleted = True

            # Step 4: Update existing or create new
            for size_data in data.size:
                size = db.query(Sizes).filter(
                    Sizes.value == size_data.value,
                    Sizes.detail_id == product_detail_id
                ).first()

                if size:
                    size.price = size_data.price
                    size.is_deleted = False  # In case it was soft-deleted earlier
                else:
                    new_size = Sizes(
                        value=size_data.value,
                        price=size_data.price,
                        detail_id=product_detail_id
                    )
                    db.add(new_size)

            db.commit()
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

