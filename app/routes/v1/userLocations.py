from app.routes.depth import PermissionChecker
from app.utils.permissions import pages_and_permissions
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.crud.userLocations import user_location
from app.schemas.userLocations import UserLocation, UserLocationCreate, UserLocationUpdate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=UserLocation, status_code=status.HTTP_201_CREATED)
def create_user_location(
    *,
    db: Session = Depends(get_db),
    user_location_in: UserLocationCreate,
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['create']))
):
    """
    Create new user location.
    """
    if user_location_in.user_id is None:
        user_location_in.user_id = current_user['id']
    user_location_obj = user_location.create(db=db, obj_in=user_location_in)
    return user_location_obj

@router.get("/{user_location_id}", response_model=UserLocation)
def get_user_location(
    *,
    db: Session = Depends(get_db),
    user_location_id: UUID,
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['view']))
):
    """
    Get user location by ID.
    """
    user_location_obj = user_location.get(db=db, id=user_location_id)
    if not user_location_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User location not found"
        )
    return user_location_obj

@router.get("/user/list", response_model=List[UserLocation])
def get_user_locations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['view']))
):
    """
    Get all locations for a specific user.
    """
    user_id = current_user['id']
    user_locations = user_location.get_by_user_id(db=db, user_id=user_id)
    return user_locations

@router.get("/user/default", response_model=UserLocation)
def get_user_default_location(
    *,
    db: Session = Depends(get_db),
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['view']))
):
    """
    Get default location for a specific user.
    """
    user_id = current_user['id']
    default_location = user_location.get_default_location(db=db, user_id=user_id)
    if not default_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No default location found for this user"
        )
    return default_location

@router.put("/{user_location_id}", response_model=UserLocation)
def update_user_location(
    *,
    db: Session = Depends(get_db),
    user_location_id: UUID,
    user_location_in: UserLocationUpdate,
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['update']))
):
    """
    Update user location.
    """
    user_location_obj = user_location.get(db=db, id=user_location_id)
    if not user_location_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User location not found"
        )
    user_location_obj = user_location.update(
        db=db, db_obj=user_location_obj, obj_in=user_location_in
    )
    return user_location_obj

@router.delete("/{user_location_id}", response_model=UserLocation)
def delete_user_location(
    *,
    db: Session = Depends(get_db),
    user_location_id: UUID,
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['delete']))
):
    """
    Delete user location.
    """
    user_location_obj = user_location.get(db=db, id=user_location_id)
    if not user_location_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User location not found"
        )
    user_location_obj = user_location.delete(db=db, id=user_location_id)
    return user_location_obj

@router.patch("/{user_location_id}/soft-delete", response_model=UserLocation)
def soft_delete_user_location(
    *,
    db: Session = Depends(get_db),
    user_location_id: UUID,
    current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['UserLocations']['delete']))
):
    """
    Soft delete user location (mark as inactive).
    """
    user_location_obj = user_location.get(db=db, id=user_location_id)
    if not user_location_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User location not found"
        )
    user_location_obj = user_location.soft_delete(db=db, id=user_location_id)
    return user_location_obj
