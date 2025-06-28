from sqlalchemy.orm import Session
from app.models.Permissions import Permissions
from app.models.PermissionPages import PermissionPages


def get_all_permissions(db: Session, page_id):
    query = db.query(Permissions)
    if page_id is not None:
        query = query.filter(Permissions.permission_page_id == page_id)

    return query.all()


def get_all_permission_pages(db: Session):
    query = db.query(PermissionPages).all()
    return query