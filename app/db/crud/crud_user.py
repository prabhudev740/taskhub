from datetime import datetime, timezone
from uuid import UUID
from core.logging_conf import Logging
from db.base import get_session
from db.models.user import UserModel

log = Logging(__name__).log()


def create_user(user_data: dict) -> UserModel:
    user = UserModel(**user_data)
    session = get_session()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(username: str) -> UserModel | None:
    session = get_session()
    user =  session.query(UserModel).where(UserModel.username == username).first()
    if not user:
        return None
    return user


def get_user_by_email(email: str) -> UserModel | None:
    session = get_session()
    user =  session.query(UserModel).where(UserModel.email == email).first()
    if not user:
        return None
    return user


def get_user_by_id(user_id: UUID) -> UserModel | None:
    session = get_session()
    print(f" ====={type(UserModel.id)}, {type(user_id)}")
    user =  session.query(UserModel).where(UserModel.id == user_id).first()
    print(user.id)
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
    user.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)
    return user


def update_user_password(hashed_password_update,
                         user_id: UUID | None = None, username: str | None = None) -> UserModel | None:
    log.info(f"user_id: {user_id}, type: {type(user_id)}\n")
    session = get_session()
    user = session.query(UserModel).where((UserModel.id == user_id) | (UserModel.username == username)).first()
    if not user:
        return None
    user.hashed_password = hashed_password_update
    user.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)
    return user

def update_login_time(user_id: UUID):
    session = get_session()
    user = session.query(UserModel).where(UserModel.id == user_id).first()
    user.last_login_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)
    return user
