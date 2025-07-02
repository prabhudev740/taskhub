""" DB during setup"""

from core.logging_conf import Logging
from core.permission_config import ORGANIZATION_ROLES, ALL_PERMISSIONS
from db.crud.crud_permission import create_permissions
from db.crud.crud_user import get_user_by_username
from db.crud.curd_role import create_role
from schemas.role import CreateRole
from schemas.user import CreateUser
from services.organization_service import map_role_permissions
from services.user_service import create_new_user

log = Logging(__name__).log()


async def create_organization_permission():
    """ Create all the default permissions to db. """
    for perm in ALL_PERMISSIONS:
        create_permissions(permission_data=perm)


async def create_default_roles_and_permissions():
    """Create default roles and update the role permission table"""
    for role_data in ORGANIZATION_ROLES.values():
        log.info(role_data)
        role = CreateRole(name=role_data['name'], description=role_data['description'])
        role = role.model_dump(exclude_unset=True)
        created_role = create_role(role)
        role_id = created_role.id
        await map_role_permissions(role_id, role_data['permissions'])


async def db_init():
    """ Init the db while running for first time. """
    admin_data = CreateUser(
        first_name="admin",
        last_name="admin",
        username="admin",
        email="admin@gmail.com",
        password="admin@123",
    )
    if not get_user_by_username(username=admin_data.username):
        await create_new_user(admin_data, is_superuser=True)
