from db.base import get_session
from db.models.permission import PermissionModel


def create_permissions(permission_data: dict) -> PermissionModel:
    permission = PermissionModel(**permission_data)
    session = get_session()
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission

def get_permission_by_name(permission_name: str) -> PermissionModel | None:
    session = get_session()
    permission = session.query(PermissionModel).filter_by(name=permission_name).first()
    if not permission:
        return None
    return permission

