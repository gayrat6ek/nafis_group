from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.roles import RolesGet


class GetUserFullData(BaseModel):
    id:Optional[UUID]=None
    full_name: Optional[str]=None
    username:Optional[str]=None
    created_at:Optional[datetime]=None
    role:Optional[RolesGet]=None
    model_config = ConfigDict(
        from_attributes=True
    )



class GetUser(BaseModel):
    id:Optional[UUID]=None
    full_name: Optional[str]=None
    username:Optional[str]=None
    model_config = ConfigDict(
        from_attributes=True
    )


