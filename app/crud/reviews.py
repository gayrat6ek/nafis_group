from pickletools import read_unicodestringnl

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
from sqlalchemy.orm import joinedload


import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.reviews import Reviews
from app.models.Products import Products
from app.schemas.reviews import CreateReview, UpdateReview

def ProductsRatingUpdate(db: Session, product_id: UUID):
    try:
        average_rating = db.query(func.avg(Reviews.rating)).filter(
            Reviews.product_id == product_id,
        ).scalar()
        # Update the product's rating
        product = db.query(Products).filter(Products.id == product_id).first()
        if product:
            product.rating = average_rating
            db.commit()
            db.refresh(product)
        
        return average_rating
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e




def create_review(db: Session, data: CreateReview,user_id) -> Reviews:
    review = db.query(Reviews).filter(
        Reviews.user_id == user_id,
        Reviews.product_id == data.product_id,
    ).first()
    
    if review:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this product."
        )
    try:
        review = Reviews(
            user_id=user_id,
            product_id=data.product_id,
            rating=data.rating,
            comment=data.comment,
            is_active=True, 
            images=data.images,  # Assuming images is a list of URLs or paths
            product_detail_id=data.product_detail_id
        )
        db.add(review)
        db.commit()
        ProductsRatingUpdate(db=db,product_id=data.product_id)
        db.refresh(review)
        return review
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_review(db: Session, review_id: UUID) -> Optional[Reviews]:
    try:
        review = db.query(Reviews).filter(Reviews.id == review_id, Reviews.is_active == True).first()
        if not review:
            return None
        return review
    
    except SQLAlchemyError as e:
        raise e
    


def update_review(db: Session, review_id: UUID, data: UpdateReview) -> Optional[Reviews]:
    try:
        review = db.query(Reviews).filter(Reviews.id == review_id).first()
        if not review:
            return None
        
        if data.rating is not None:
            review.rating = data.rating
        if data.comment is not None:
            review.comment = data.comment
        if data.images is not None:
            review.images = data.images  # Update images if provided
        
        db.commit()
        db.refresh(review)
        return review
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e 
    


def delete_review(db: Session, review_id: UUID) -> Optional[Reviews]:
    try:
        review = db.query(Reviews).filter(Reviews.id == review_id).first()
        if not review:
            return None
        
        review.is_active = False  # Soft delete by marking as inactive
        db.commit()
        db.refresh(review)
        return review
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e 
    



def get_reviews(db: Session, product_id:Optional[UUID]=None, user_id:Optional[UUID]=None, is_active: Optional[bool] = None,page: int = 1, size: int = 10) -> list[Reviews]:
    try:
        query = db.query(Reviews)
        
        if is_active is not None:
            query = query.filter(Reviews.is_active == is_active)
        if product_id:
            query = query.filter(Reviews.product_id == product_id)
        if user_id:
            query = query.filter(Reviews.user_id == user_id)
        query = query.order_by(Reviews.created_at.desc())
        
        # Pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        return {
            "items": query.all(),
            "total": query.count(),
            "page": page,
            "size": size,
            "pages": (query.count() + size - 1) // size  # Calculate total pages    
        }
    
    except SQLAlchemyError as e:
        raise e 
    

def admin_get_reviews(db: Session, order_id, page: int = 1, size: int = 10,):
    try:
        query = db.query(Reviews).order_by(Reviews.created_at.desc())
        if order_id:
            query = query.filter(Reviews.id == order_id)
        query = query.options(
            joinedload(Reviews.product),
            joinedload(Reviews.product_detail)  # for direct detail
        )
        
        # Pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        count = query.count()
        all_reviews = query.all()
        for review in all_reviews:
            

            # decide which details to include
            if review.product_detail_id:
                # only the specific detail
                review.product.details = [review.product_detail]
               
        
        return {
            "items": all_reviews,
            "total": count,
            "page": page,
            "size": size,
            "pages": (count + size - 1) // size  # Calculate total pages    
        }
    
    except SQLAlchemyError as e:
        raise e
    