from contextlib import asynccontextmanager

import pytz
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.pages_and_permissions import (
    create_permission_page,
    create_permission,
    get_permission_page,
    get_permission,
    get_permission_link
)
from app.crud.roles import create_role,  get_role_by_name,update_role
from app.crud.users import create_user, get_user_by_username
from app.schemas.roles import UpdateRole
from app.routes.depth import get_db
from app.utils.permissions import pages_and_permissions

timezonetash = pytz.timezone('Asia/Tashkent')


# #create new permission
# @asynccontextmanager
# async def create_permissions_lifespan():
#     db: Session = next(get_db())
#     for key, value in pages_and_permissions.items():
#         permission_page = get_permission_page(db=db, name=key)
#         if permission_page:
#             permission_page_id = permission_page.id
#         else:
#             permission_page_id = create_permission_page(db=db, name=key).id
#         for name, link in value.items():
#             permission = get_permission(db=db, link=link, permission_page_id=permission_page_id)
#             if not permission:
#                 create_permission(db=db, name=name, link=link, permission_page_id=permission_page_id)

#     yield  #--------------  HERE YOU CAN WRITE LOG ON CLOSING AFTER YIELD ------------


#---------------------- CREATE ROLE AND USERS FOR DEFAULT ADMIN USER --------------------------
@asynccontextmanager
async def create_role_lifespan():
    db: Session = next(get_db())
    role_permissions = []
    for key, value in pages_and_permissions.items():
        for name, link in value.items():
            role_permissions.append(link)

    role = get_role_by_name(db=db, name=settings.admin_role)
    if not role:
        role = create_role(db=db, name=settings.admin_role, description='Admin',permissions=role_permissions)
    else:
        role = update_role(db=db, id=role.id,data=UpdateRole(**{
    'name': settings.admin_role,
    'description': 'Admin',
    'permissions': role_permissions
}))

    user = get_user_by_username(db=db, username=settings.admin_role)
    if not user:
        create_user(db=db, username=settings.admin_role, password=settings.admin_password, role_id=role.id,
                    fullname='Admin user')

    # role_permissions = []
    # for i in role.access:
    #     role_permissions.append(i.permission.link)

    # for key, value in pages_and_permissions.items():
    #     for name, link in value.items():
    #         if link not in role_permissions:
    #             permission = get_permission_link(db=db, link=link)

    #             create_accesses(db=db, role_id=role.id, permission_id=permission.id)

    yield  #--------------  HERE YOU CAN WRITE LOG ON CLOSING AFTER YIELD ------------


# async def daily_run():
#     scheduler = BackgroundScheduler()
#
#     scheduler.start()
#     return True
#
#
# @asynccontextmanager
# async def run_scheduler():
#     await daily_run()
#     yield


@asynccontextmanager
async def combined_lifespan(app):
    async with  create_role_lifespan():
        #-----------   BEFORE YIELD WHEN STARTING UP ALL THE FUNCTIONS WORK ---------
        yield
