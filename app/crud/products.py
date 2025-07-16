from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
from app.models.Products import Products
from app.models.discounts import Discounts
from app.models.discountProducts import DiscountProducts

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.Products import Products
from app.schemas.products import CreateProduct, UpdateProduct
from app.utils.utils import timezonetash
from app.models.productMaterials import ProductMaterials


def create_product(db: Session, data: CreateProduct) -> Products:
    try:
        product = Products(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            description_en=data.description_en,
            description_ru=data.description_ru,
            description_uz=data.description_uz,
            is_active=True,
            loan_accessable=data.loan_accessable,
            delivery_days=data.delivery_days,
            category_id=data.category_id,
            brand_id=data.brand_id,
        )
        #here whe should add materials if provided and after getting the product id
        db.add(product)
        db.commit()
        db.refresh(product) 
        if data.materials:
            for material in data.materials:
                product_material = ProductMaterials(
                    product_id=product.id,
                    material_id=material
                )
                db.add(product_material)
            db.commit()
            db.refresh(product)
        return product
    except SQLAlchemyError as e:
        db.rollback()
        raise e
        


    
    
from sqlalchemy.orm import joinedload
from datetime import datetime

def get_products(
    db: Session,
    page: int = 1,
    size: int = 10,
    is_active: Optional[bool] = None
):
    try:
        now = datetime.now(timezonetash)

        query = db.query(Products).options(
            joinedload(Products.discounts).joinedload(DiscountProducts.discount)
        )

        if is_active is not None:
            query = query.filter(Products.is_active == is_active)

        total_count = query.count()
        products = query.offset((page - 1) * size).limit(size).all()

        # Filter each product's discounts in Python
        for product in products:
            product.discounts = [
                dp for dp in product.discounts
                if dp.discount.is_active and dp.discount.active_from <= now and dp.discount.active_to >= now
            ]

        return {
            "items": products,
            "total": total_count,
            "page": page,
            "size": size,
            "pages": (total_count + size - 1) // size
        }

    except SQLAlchemyError as e:
        raise e

def get_product_by_id(db: Session, product_id: UUID) -> Optional[Products]:
    try:
        return db.query(Products).filter(Products.id == product_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_product(db: Session, product_id: UUID, data: UpdateProduct) -> Optional[Products]:
    try:
        product = db.query(Products).filter(Products.id == product_id).first()
        if not product:
            return None
        
        if data.name_en is not None:
            product.name_en = data.name_en
        if data.name_ru is not None:
            product.name_ru = data.name_ru
        if data.name_uz is not None:
            product.name_uz = data.name_uz
        if data.description_en is not None:
            product.description_en = data.description_en
        if data.description_ru is not None:
            product.description_ru = data.description_ru
        if data.description_uz is not None:
            product.description_uz = data.description_uz
        if data.is_active is not None:
            product.is_active = data.is_active
        if data.loan_accessable is not None:
            product.loan_accessable = data.loan_accessable
        if data.delivery_days is not None:
            product.delivery_days = data.delivery_days
        if data.category_id is not None:
            product.category_id = data.category_id
        if data.brand_id is not None:
            product.brand_id = data.brand_id
        
        db.commit()
        db.refresh(product)
        if data.materials:
            # Clear existing materials
            db.query(ProductMaterials).filter(ProductMaterials.product_id == product.id).delete()
            db.commit()
            
            # Add new materials
            for material in data.materials:
                product_material = ProductMaterials(
                    product_id=product.id,
                    material_id=material
                )
                db.add(product_material)
            db.commit()
            db.refresh(product)
        return product
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e