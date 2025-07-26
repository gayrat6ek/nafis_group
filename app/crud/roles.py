from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.Roles import Roles
from app.schemas.roles import CreateRole, UpdateRole


def create_role(db:Session, name, description,permissions: Optional[list[UUID]] = []):
    query = Roles(
        name=name,
        description=description,
        is_active=True,
        permissions=permissions 
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return  query



def get_role_by_name(db:Session,name):
    query = db.query(Roles).filter(Roles.name==name).first()
    return query







def get_all_roles(db: Session):
    query = db.query(Roles).all()
    return query


def get_one_role(db: Session, role_id):
    query = db.query(Roles).get(role_id)
    return query


def add_role(db:Session, data: CreateRole):
    try:
        role = Roles(
            name=data.name,
            description=data.description,
            is_active=data.is_active,
            permissions=data.permissions if data.permissions else []
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None


def update_role(db:Session, data: UpdateRole,id: UUID):
    role = db.query(Roles).get(id)
    if data.name is not None:
        role.name = data.name
    if data.description is not None:
        role.description = data.description
    if data.is_active is not None:
        role.is_active = data.is_active
    if data.permissions is not None:
        role.permissions = data.permissions if data.permissions else []

    db.commit()
    db.refresh(role)

    return role
