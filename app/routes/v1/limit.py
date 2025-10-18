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

from app.routes.depth import get_db, PermissionChecker
from app.crud import limit as crud_limit
from app.schemas.limit import Limit
from app.utils.permissions import pages_and_permissions

limit_router = APIRouter()

@limit_router.get('/limit')
async def get_limit(
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Limits']['view']))
):
    limit = crud_limit.get_limit(db=db)
    return limit


@limit_router.post('/limit')
async def create_or_update_limit(
    limit: Limit,
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Limits']['create']))
):
    limit = crud_limit.create_or_update_limit(db=db, limit=limit.limit)
    return limit