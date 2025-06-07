from uuid import UUID

from db.base import get_session
from db.models.user import UserModel


def create_user(user_data: dict) -> UserModel:
    user = UserModel(**user_data)
    session = get_session()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(email: str):
    session = get_session()
    user =  session.query(UserModel).where(UserModel.email == email).first()
    if not user:
        return None
    return user


def get_user_by_id(user_id: str):
    session = get_session()
    user =  session.query(UserModel).where(UserModel.id == user_id).first()
    if not user:
        return None
    return user


def update_user(user_id: UUID, user_data: dict) -> UserModel | None:
    session = get_session()
    user = session.query(UserModel).where(UserModel.id==user_id).first()
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user

