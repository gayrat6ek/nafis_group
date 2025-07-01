from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict




class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class ProductGet(BaseConfig):
    id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None