from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
from app.models.Products import Products
from app.models.discounts import Discounts
from app.models.discountProducts import DiscountProducts
from app.models.Categories import Categories
from app.models.Brands import Brands
from app.models.likes import Likes
from app.models.productDetails import ProductDetails
from app.models.sizes import Sizes
from sqlalchemy.orm import selectinload, with_loader_criteria
from app.crud.categories import get_category_with_children
from app.models.materials import Materials

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.Products import Products
from app.schemas.products import CreateProduct, OrderBy, ProductFilter, UpdateProduct
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
            characteristics=data.characteristics,  # Assuming characteristics is a JSON object
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
    filter: ProductFilter = None,

):
    try:
        now = datetime.now(timezonetash)

        query = (
            db.query(Products)
            .options(
                # Load discounts through DiscountProducts
                joinedload(Products.discounts)
                .joinedload(DiscountProducts.discount),
                
                # Only include discounts that are currently active
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

                # Eager-load product details
                joinedload(Products.details)
                .joinedload(ProductDetails.size),

                # Filter sizes: only sizes not marked as deleted
                with_loader_criteria(
                    Sizes,
                    lambda s: s.is_deleted == False,
                    include_aliases=True
                )
            )
        )

        if filter.is_active is not None:
            query = query.filter(Products.is_active == filter.is_active)
        if filter.category_id is not None:
            category_ids = get_category_with_children(db, filter.category_id)
            query = query.filter(Products.category_id.in_(category_ids))
        if filter.brands is not None:
            query = query.filter(Products.brand_id.in_(filter.brands))
        if filter.materials is not None:
            query = query.filter(Products.materials.any(Materials.id.in_(filter.materials)))
        if filter.price_from is not None:
            query = query.filter(Products.details.any(ProductDetails.size.any(Sizes.price >= filter.price_from)))
        if filter.price_to is not None:
            query = query.filter(Products.details.any(ProductDetails.size.any(Sizes.price <= filter.price_to)))
        if filter.order_by is not None:
            if filter.order_by == OrderBy.price_asc:
                query = query.order_by(Products.price.asc())
            elif filter.order_by == OrderBy.price_desc:
                query = query.order_by(Products.price.desc())
            elif filter.order_by == OrderBy.views_desc:
                query = query.order_by(Products.views.desc())
            elif filter.order_by == OrderBy.views_asc:
                query = query.order_by(Products.views.asc())
            elif filter.order_by == OrderBy.created_at_desc:
                query = query.order_by(Products.created_at.desc())
            elif filter.order_by == OrderBy.created_at_asc:
                query = query.order_by(Products.created_at.asc())
            
            

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
        now = datetime.now(timezonetash)

        product = (
            db.query(Products)
            .options(
                joinedload(Products.discounts)
                .joinedload(DiscountProducts.discount),

                with_loader_criteria(
                    DiscountProducts,
                    lambda dp: dp.discount.has(
                        and_(
                            Discounts.is_active == True,
                            Discounts.active_from <= now,
                            Discounts.active_to >= now
                        )
                    ),
                    include_aliases=True
                ),

                joinedload(Products.details)
                .joinedload(ProductDetails.size),

                with_loader_criteria(
                    Sizes,
                    lambda s: s.is_deleted == False,
                    include_aliases=True
                )
            )
            .filter(Products.id == product_id)
            .first()
        )
        if product and not product.views:
            product.views = 1  # Initialize views if not set
        else:
            product.views += 1
        db.commit()  # Commit the view increment    
        db.refresh(product)  # Refresh to get the updated views count


        product.reviews = product.reviews[:6]
        return product
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
        # if data.characteristics is not None:
        product.characteristics = data.characteristics
        
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
    

def get_liked_products(db: Session, user_id: UUID, page: int = 1, size: int = 10):
    try:
        query = db.query(Products).join(Products.likes).filter(Likes.user_id == user_id)
        
        total_count = query.count()
        query = query.order_by(Products.created_at.desc())
        products = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": products,
            "total": total_count,
            "page": page,
            "size": size,
            "pages": (total_count + size - 1) // size
        }
    except SQLAlchemyError as e:
        raise e         
    

def search_products(
    db: Session,
    query: str,
    page: int = 1,
    size: int = 10,
    is_active: Optional[bool] = None
):
    try:
        search_query = f"%{query}%"
        product_query = db.query(Products).join(Products.category).join(Products.brand).filter(
            or_(
                Products.name_en.ilike(search_query),
                Products.name_ru.ilike(search_query),
                Products.name_uz.ilike(search_query),
                Products.description_en.ilike(search_query),
                Products.description_ru.ilike(search_query),
                Products.description_uz.ilike(search_query),
                Categories.name_en.ilike(search_query),
                Categories.name_ru.ilike(search_query),
                Categories.name_uz.ilike(search_query),
                Brands.name_en.ilike(search_query),
                Brands.name_ru.ilike(search_query),
                Brands.name_uz.ilike(search_query)
            )
        )



        if is_active is not None:
            product_query = product_query.filter(Products.is_active == is_active)

        total_count = product_query.count()
        products = product_query.offset((page - 1) * size).limit(size).all()

        return {
            "items": products,
            "total": total_count,
            "page": page,
            "size": size,
            "pages": (total_count + size - 1) // size
        }
    except SQLAlchemyError as e:
        raise e
    


