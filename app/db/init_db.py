""" DB during setup"""

from uuid import UUID
from core.logging_conf import Logging
from core.permission_config import ORGANIZATION_ROLES, ALL_PERMISSIONS
from db.crud.crud_permission import create_permissions, get_permission_by_name
from db.crud.crud_user import get_user_by_username
from db.crud.curd_role import create_role, update_role_permission, get_role_by_name
from schemas.user import CreateUser
from services.user_service import create_new_user

log = Logging(__name__).log()


async def create_organization_permission():
    """ Create all the default permissions to db. """
    for perm in ALL_PERMISSIONS:
        create_permissions(permission_data=perm)


async def update_default_role_permission(role_id: UUID, permissions: list[str]):
    """Update the role_permission table"""
    for perm_name in permissions:
        permission = get_permission_by_name(permission_name=perm_name)
        update_role_permission(role_id, permission.id)


async def create_default_roles_and_permissions():
    """Create default roles and update the role permission table"""
    for role_data in ORGANIZATION_ROLES.values():
        log.info(role_data)
        created_role = create_role(name=role_data['name'], description=role_data['description'])
        role_id = created_role.id
        await update_default_role_permission(role_id, role_data['permissions'])


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

    # Create permissions only if not present
    for perm in ALL_PERMISSIONS:
        if not get_permission_by_name(permission_name=perm['name']):
            create_permissions(permission_data=perm)

    # Create roles and assign permissions only if role not present
    for role_data in ORGANIZATION_ROLES.values():
        if not get_role_by_name(role_data['name']):
            created_role = create_role(name=role_data['name'], description=role_data['description'])
            role_id = created_role.id
            await update_default_role_permission(role_id, role_data['permissions'])
