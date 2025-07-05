

from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.crud import colors as crud_colors
from app.routes.depth import get_db, PermissionChecker
from app.schemas.colors import ColorGet, ColorList, CreateColor, UpdateColor
from app.models.colors import Colors
from app.utils.permissions import pages_and_permissions


colors_router = APIRouter()


@colors_router.get('/colors', response_model=List[ColorList])
async def get_color_list(

        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Colors']['view']))
):
    return crud_colors.get_colors(db=db, is_active=is_active)



@colors_router.get('/colors/{id}', response_model=ColorGet)
async def get_color(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Colors']['view']))
):
    color = crud_colors.get_color_by_id(db=db, color_id=id)
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color


@colors_router.post('/colors', response_model=ColorGet)
async def create_color(
        body: CreateColor,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Colors']['create']))
):
    created_color = crud_colors.create_color(db=db, data=body)
    return created_color


@colors_router.put('/colors/{id}', response_model=ColorGet)
async def update_color(
        id: UUID,
        body: UpdateColor,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Colors']['update']))
):
    color = crud_colors.get_color_by_id(db=db, color_id=id)
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    
    updated_color = crud_colors.update_color(db=db, color_id=id, data=body)
    return updated_color    