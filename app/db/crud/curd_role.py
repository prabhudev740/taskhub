""" CRUD User """

from uuid import UUID
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

def get_role_by_role_name_team_id(role_name: str, team_id: UUID) -> type[RoleModel] | None:
    """
    Retrieve the role by role id.

    Args:
        role_name (str): The role name to get the id.
        team_id (UUID): The ID of the team.

    Returns:
        type[RoleModel] | None: The role for the specific ID.
    """
    session = get_session()
    role = session.query(RoleModel).filter_by(name=role_name, team_id=team_id).first()
    if not role:
        return None
    return role

def get_roles_by_org_id(org_id: UUID) -> list[type[RoleModel]] | None:
    """
    Retrieve a role by the organization.

    Args:
        org_id (UUID): The ID of the organization.
    Returns:
        list[RoleModel] | None: The role if found, otherwise None.
    """
    session = get_session()
    roles = session.query(RoleModel).filter_by( organization_id=org_id).all()
    if not roles:
        return None
    return roles


def get_role_by_id(role_id: UUID) -> RoleModel | None:
    """
    Retrieve a role by its id.

    Args:
        role_id (UUID): The id of the role to retrieve.

    Returns:
        RoleModel | None: The role if found, otherwise None.
    """
    session = get_session()
    role = session.query(RoleModel).get(role_id)
    if not role:
        return None
    return role


def get_all_organization_roles(organization_id: UUID) -> list[type[RoleModel]] | None:
    """
    Retrieve a role by its id.

    Args:
        organization_id (UUID): The ID of the organization.

    Returns:
        list[RoleModel] | None: The roles if found, otherwise None.
    """
    session = get_session()
    roles = session.query(RoleModel).filter_by(organization_id=organization_id).all()
    if not roles:
        return None
    return roles


def update_role_permission(role_id: UUID, permission_id: UUID) -> RolePermissionModel:
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
                        ) -> type[RolePermissionModel] | None:
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
        role_id=role_id, permission_id=permission_id).first()
    if not role_permission:
        return None
    return role_permission

def get_permission_ids_for_role(role_id: UUID) -> list[UUID] | None:
    """
    Retrieve the permission ids assigned to a role.

    Args:
        role_id (UUID): The ID of the role.

    Returns:
        list[UUID] | None: The list of permission IDs or None.
    """
    session = get_session()
    results = session.query(RolePermissionModel.permission_id).filter_by(role_id=role_id).all()
    if not results:
        return None
    return [row.permission_id for row in results]
