from uuid import UUID
from core.logging_conf import Logging
from db.base import get_session
from db.models.role import RoleModel, RolePermissionModel

log = Logging(__name__).log()


def create_role(name=str, description=str) -> RoleModel:
    role = RoleModel(name=name, description=description)
    session = get_session()
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

def get_role_by_name(role_name: str) -> RoleModel | None:
    session = get_session()
    role = session.query(RoleModel).filter_by(name=role_name).first()
    if not role:
        return None
    return role

def update_role_permission(role_id: UUID, permission_id: UUID):
    role_permission = RolePermissionModel(role_id=role_id, permission_id=permission_id)
    session = get_session()
    session.add(role_permission)
    session.commit()
    session.refresh(role_permission)
    return role_permission


def get_role_permission(role_id: UUID, permission_id: UUID) -> RolePermissionModel | None:
    session = get_session()
    role_permission = session.query(RolePermissionModel).filter_by(role_id=role_id, permission_id=permission_id)
    if not role_permission:
        return None
    return role_permission


# if __name__ == "__main__":
    # create_role("owner")
