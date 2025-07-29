
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
from app.crud import categories as crud_categories
from app.routes.depth import get_db, PermissionChecker
from app.schemas.categories import CategoryGet, CategoryList, CreateCategory, UpdateCategory,FilterCategory,GetCategoriesTree,GetCategoriesTreeReversed
from app.models.Categories import Categories
from app.utils.permissions import pages_and_permissions



categories_router = APIRouter()



@categories_router.get('/categories', response_model=List[CategoryList])
async def get_category_list(

        filter: FilterCategory = Depends(),
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['view']))
):
    return crud_categories.get_categories(db=db, filter=filter)


@categories_router.get('/category/{id}', response_model=CategoryGet)
async def get_category(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['view']))
):
    category = crud_categories.get_category_by_id(db=db, category_id=id)
    return category


@categories_router.post('/categories', response_model=CategoryGet)
async def create_category(
        body: CreateCategory,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['create']))
):
    created_category = crud_categories.create_category(db=db, data=body)
    return created_category


@categories_router.put('/categories/{id}', response_model=CategoryGet)
async def update_category(
        id: UUID,
        body: UpdateCategory,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['update']))
):
    category = crud_categories.get_category_by_id(db=db, category_id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    updated_category = crud_categories.update_category(db=db, category_id=id, data=body)
    return updated_category


@categories_router.get('/categories/tree', response_model=List[GetCategoriesTree])
async def get_category_tree(

        filter: FilterCategory = Depends(),
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['view']))
):
    categories = crud_categories.get_categories(db=db, filter=filter)
    return categories



@categories_router.get('/categories/reversed/tree', response_model=List[GetCategoriesTreeReversed])
async def get_category_tree(

        filter: FilterCategory = Depends(),
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['view']))
):
    categories = crud_categories.get_categories(db=db, filter=filter)
    return categories


@categories_router.get('/categories/tree/{id}', response_model=GetCategoriesTree)
async def get_category_tree_by_id(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['view']))
):
    category = crud_categories.get_category_by_id(db=db, category_id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category



@categories_router.get('/categories/reversed/tree/{id}', response_model=GetCategoriesTreeReversed)
async def get_category_tree_by_id(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Categories']['view']))
):
    category = crud_categories.get_category_by_id(db=db, category_id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category





