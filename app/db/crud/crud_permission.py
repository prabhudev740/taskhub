""" Doc """
from uuid import UUID
from db.base import get_session
from db.models.permission import PermissionModel


def create_permissions(permission_data: dict) -> PermissionModel:
    """
    Create a new permission in the database.

    Args:
        permission_data (dict): A dictionary containing the details of the permission.

    Returns:
        PermissionModel: The newly created permission.
    """
    permission = PermissionModel(**permission_data)
    session = get_session()
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission


def get_permission_by_name(permission_name: str) -> type[PermissionModel] | None:
    """
    Retrieve a permission by its name.

    Args:
        permission_name (str): The name of the permission to retrieve.

    Returns:
        type[PermissionModel] | None: The permission if found, otherwise None.
    """
    session = get_session()
    permission = session.query(PermissionModel).filter_by(name=permission_name).first()
    if not permission:
        return None
    return permission

def get_permission_by_id(permission_id: UUID) -> type[PermissionModel] | None:
    """
    Retrieve a permission by its name.

    Args:
        permission_id (str): The name of the permission to retrieve.

    Returns:
        type[PermissionModel] | None: The permission if found, otherwise None.
    """
    session = get_session()
    permission = session.query(PermissionModel).filter_by(id=permission_id).first()
    if not permission:
        return None
    return permission
