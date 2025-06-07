from uuid import UUID

from db.base import get_session
from db.models.user import User


def create_user(first_name: str, last_name: str, email: str, hashed_password: str) -> User:
    user = User(first_name=first_name,
                last_name=last_name,
                email=email,
                hashed_password=hashed_password)

    session = get_session()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(email: str):
    session = get_session()
    user =  session.query(User).where(User.email == email).first()
    return user


def update_user(user_id: UUID, updated_date: dict):
    session = get_session()
    user = session.query(User).where(User.id==user_id).first()
    user.update(updated_date)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(id: str):
    pass

