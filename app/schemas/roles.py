from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class PermissionsGet(BaseConfig):
    id:Optional[UUID]=None
    name:Optional[str]=None
    link : Optional[str]=None


class GetPermissionPage(BaseConfig):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    permission: Optional[List[PermissionsGet]] = None


class AccessesGet(BaseConfig):
    id:UUID
    permission:Optional[PermissionsGet]=None



class RolesGet(BaseConfig):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    created_at : Optional[datetime] = None
    # access: Optional[list[str]] = None
    permissions : Optional[List[str]] = None


class RoleList(BaseConfig):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
    created_at : Optional[datetime] = None
    is_active: Optional[bool] = True


class CreateRole(BaseConfig):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    permissions: Optional[List[str]] = None



class UpdateRole(BaseConfig):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    permissions: Optional[List[str]] = None
