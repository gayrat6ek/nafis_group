from typing import List, Optional
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
from app.routes.depth import get_db, PermissionChecker
from app.crud import materials as crud_materials
from app.schemas.materials import (
    MaterialsGet, 
    MaterialsList,
    CreateMaterials,
    UpdateMaterials,
)


from app.models.materials import Materials
from app.utils.permissions import pages_and_permissions 


materials_router = APIRouter()

@materials_router.get('/materials', response_model=Page[MaterialsList])
async def get_materials_list(
        is_active: bool = None,
        page: int = 1,
        size: int = 10,
        name:Optional[str] = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Materials']['view']))
):
    return crud_materials.get_materials(db=db, is_active=is_active,name=name, page=page, size=size)



@materials_router.get('/materials/{id}', response_model=MaterialsGet)
async def get_material(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Materials']['view']))
):
    material = crud_materials.get_material_by_id(db=db, material_id=id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@materials_router.post('/materials', response_model=MaterialsGet)
async def create_material(
        body: CreateMaterials,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Materials']['create']))
):
    created_material = crud_materials.create_material(db=db, data=body)
    return created_material

@materials_router.put('/materials/{id}', response_model=MaterialsGet)
async def update_material(  
        id: UUID,
        body: UpdateMaterials,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Materials']['update']))
):
    updated_material = crud_materials.update_material(db=db, material_id=id, data=body)
    if not updated_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated_material
