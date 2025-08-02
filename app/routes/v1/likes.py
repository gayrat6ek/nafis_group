from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud import likes as crud_likes
from app.routes.depth import get_db, PermissionChecker
from app.schemas.likes import (
    AddRemoveLike
)
from app.utils.permissions import pages_and_permissions



likes_router = APIRouter()

@likes_router.post('/likes', )
async def add_remove_like(
        body: AddRemoveLike,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Likes']['create']))
):
    """
    Add or remove a like for a product.
    If the user has already liked the product, it will be removed.
    If not, it will be added.
    """
    crud_likes.add_like(
        db=db,
        user_id=current_user['id'],
        data=body
    )
    return {
        "message": "Like added or removed successfully",
        "product_id": body.product_id
    }

