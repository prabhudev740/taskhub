""" CRUD User """
from uuid import UUID
from sqlalchemy.orm import Query

from core.logging_conf import Logging
from db.base import get_session
from db.models.role import RoleModel, RolePermissionModel

log = Logging(__name__).log()


def create_role(role: dict) -> RoleModel:
    """
    Create a new role in the database.

    Args:
        role (dict): A dictionary containing role details.

    Returns:
        RoleModel: The newly created role.
    """
    role = RoleModel(**role)
    session = get_session()
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def get_role_by_name(role_name: str) -> list[type[RoleModel]] | None:
    """
    Retrieve a role by its name.

    Args:
        role_name (str): The name of the role to retrieve.

    Returns:
        RoleModel | None: The role if found, otherwise None.
    """
    session = get_session()
    roles = session.query(RoleModel).filter_by(name=role_name).all()
    if not roles:
        return None
    return roles

def get_role_by_role_name_org_id(role_name: str, org_id: UUID) -> type[RoleModel] | None:
    """
    Retrieve a role by its name.

    Args:
        role_name (str): The name of the role to retrieve.
        org_id (UUID): The ID of the organization.
    Returns:
        RoleModel | None: The role if found, otherwise None.
    """
    session = get_session()
    role = session.query(RoleModel).filter_by(name=role_name, organization_id=org_id).first()
    if not role:
        return None
    return role


def get_role_by_id(role_id: UUID) -> type[RoleModel] | None:
    """
    Retrieve a role by its id.

    Args:
        role_id (UUID): The id of the role to retrieve.

    Returns:
        RoleModel | None: The role if found, otherwise None.
    """
    session = get_session()
    role = session.query(RoleModel).filter_by(id=role_id).first()
    if not role:
        return None
    return role


def update_role_permission(role_id: UUID, permission_id: UUID):
    """
    Add a permission to a role.

    Args:
        role_id (UUID): The ID of the role.
        permission_id (UUID): The ID of the permission.

    Returns:
        RolePermissionModel: The updated role permission association.
    """
    role_permission = RolePermissionModel(role_id=role_id, permission_id=permission_id)
    session = get_session()
    session.add(role_permission)
    session.commit()
    session.refresh(role_permission)
    return role_permission


def get_role_permission(role_id: UUID, permission_id: UUID
                        ) -> Query[type[RolePermissionModel]] | None:
    """
    Retrieve the association between a role and a permission.

    Args:
        role_id (UUID): The ID of the role.
        permission_id (UUID): The ID of the permission.

    Returns:
        RolePermissionModel | None: The role permission association if found, otherwise None.
    """
    session = get_session()
    role_permission = session.query(RolePermissionModel).filter_by(
        role_id=role_id, permission_id=permission_id)
    if not role_permission:
        return None
    return role_permission
