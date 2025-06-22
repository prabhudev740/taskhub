from db.base import get_session
from db.models.role import RoleModel


def create_role(role_name: str) -> RoleModel:
    role = RoleModel(name=role_name)
    session = get_session()
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

def get_role_by_name(role_name: str) -> RoleModel:
    session = get_session()
    role = session.query(RoleModel).where(RoleModel.name == role_name).first()
    return role


if __name__ == "__main__":
    create_role("owner")
