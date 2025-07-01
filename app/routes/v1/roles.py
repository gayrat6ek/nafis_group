from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.roles import get_all_roles, get_one_role, add_role, update_role
from app.routes.depth import get_db, PermissionChecker
from app.schemas.roles import RolesGet, CreateRole, RoleList, UpdateRole
from app.utils.permissions import pages_and_permissions


roles_router = APIRouter()


@roles_router.get('/roles', response_model=List[RoleList])
async def get_role_list(
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Roles']['view']))
):
    roles = get_all_roles(db=db)
    return roles


@roles_router.get('/roles/{id}', response_model=RolesGet)
async def get_role(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Roles']['view']))
):
    role = get_one_role(db=db, role_id=id)
    return role


@roles_router.post('/roles', response_model=RolesGet)
async def create_roles(
        body: CreateRole,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Roles']['create']))
):
    created_role = add_role(db=db, data=body)
    return created_role


@roles_router.put('/roles/{id}', response_model=RolesGet)
async def update_roles(
        id: UUID,
        body: UpdateRole,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Roles']['update']))
):
    updated_role = update_role(db=db, data=body)
    return updated_role


@roles_router.get('/permissions')
async def get_permissions(
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Permissions']['view']))
):
    
    return pages_and_permissions
