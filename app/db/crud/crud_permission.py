from db.base import get_session
from db.models.permission import PermissionModel


def create_permissions(permission_data: dict):
    permission = PermissionModel(**permission_data)
    session = get_session()
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission

