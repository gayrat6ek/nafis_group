from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.crud import reviews as crud_reviews
from app.routes.depth import get_db, PermissionChecker
from app.schemas.reviews import CreateReview,ReviewGet,UpdateReview




from app.utils.permissions import pages_and_permissions

reviews_router = APIRouter()    



@reviews_router.post('/reviews', response_model=ReviewGet)
async def create_review(
        body: CreateReview,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Reviews']['create']))
):
    created_review = crud_reviews.create_review(db=db, data=body,user_id=current_user['id'])
    return created_review


@reviews_router.get('/reviews/{id}', response_model=ReviewGet)
async def get_review(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Reviews']['view']))
):
    review = crud_reviews.get_review(db=db, review_id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@reviews_router.put('/reviews/{id}', response_model=ReviewGet)
async def update_review(
        id: UUID,
        body: UpdateReview,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Reviews']['update']))
):
    updated_review = crud_reviews.update_review(db=db, review_id=id, data=body)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review


@reviews_router.get('/reviews', response_model=Page[ReviewGet])
async def get_reviews_list(
        product_id: UUID = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Reviews']['view']))
):
    reviews = crud_reviews.get_reviews(db=db, product_id=product_id)
    return reviews


@reviews_router.delete('/reviews/{id}', response_model=None)
async def delete_review(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Reviews']['delete']))
):
    deleted_review = crud_reviews.delete_review(db=db, review_id=id)
    if not deleted_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}   


@reviews_router.get('/admin/reviews/view', response_model=Page[ReviewGet])
async def admin_get_reviews_list(
        order_id: UUID = None,
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Reviews']['admin_review_view']))
):
    reviews = crud_reviews.admin_get_reviews(db=db, size=size, page=page, order_id=order_id)
    return reviews