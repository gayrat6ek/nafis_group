from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict




class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )