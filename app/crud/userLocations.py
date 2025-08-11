from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from uuid import UUID

from app.models.userLocations import UserLocations
from app.schemas.userLocations import UserLocationCreate, UserLocationUpdate

class CRUDUserLocation:
    def get(self, db: Session, id: UUID) -> Optional[UserLocations]:
        return db.query(UserLocations).filter(UserLocations.id == id).first()
    
    def get_by_user_id(self, db: Session, user_id: UUID) -> List[UserLocations]:
        return db.query(UserLocations).filter(UserLocations.user_id == user_id).all()
    
    def get_default_location(self, db: Session, user_id: UUID) -> Optional[UserLocations]:
        return db.query(UserLocations).filter(
            and_(
                UserLocations.user_id == user_id,
                UserLocations.is_default == True,
                UserLocations.is_active == True
            )
        ).first()
    
    def create(self, db: Session, *, obj_in: UserLocationCreate) -> UserLocations:
        # If this is set as default, unset other default locations for this user
        if obj_in.is_default:
            db.query(UserLocations).filter(
                and_(
                    UserLocations.user_id == obj_in.user_id,
                    UserLocations.is_default == True
                )
            ).update({"is_default": False})
        
        db_obj = UserLocations(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: UserLocations, obj_in: UserLocationUpdate) -> UserLocations:
        update_data = obj_in.dict(exclude_unset=True)
        
        # If this is being set as default, unset other default locations for this user
        if update_data.get("is_default"):
            db.query(UserLocations).filter(
                and_(
                    UserLocations.user_id == db_obj.user_id,
                    UserLocations.id != db_obj.id,
                    UserLocations.is_default == True
                )
            ).update({"is_default": False})
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: UUID) -> UserLocations:
        obj = db.query(UserLocations).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def soft_delete(self, db: Session, *, id: UUID) -> UserLocations:
        obj = db.query(UserLocations).get(id)
        obj.is_active = False
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

user_location = CRUDUserLocation()
