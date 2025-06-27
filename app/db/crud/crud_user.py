""" User model """
from datetime import datetime, timezone
from uuid import UUID
from core.logging_conf import Logging
from db.base import get_session
from db.models.user import UserModel

log = Logging(__name__).log()


def create_user(user_data: dict) -> UserModel:
    """
    Create a new user in the database.

    Args:
        user_data (dict): A dictionary containing user details.

    Returns:
        UserModel: The newly created user.
    """
    user = UserModel(**user_data)
    session = get_session()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(username: str) -> type[UserModel] | None:
    """
    Retrieve a user by their username.

    Args:
        username (str): The username of the user.

    Returns:
        UserModel | None: The user if found, otherwise None.
    """
    session = get_session()
    user = session.query(UserModel).filter_by(username=username).first()
    if not user:
        return None
    return user


def get_user_by_email(email: str) -> type[UserModel] | None:
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user.

    Returns:
        UserModel | None: The user if found, otherwise None.
    """
    session = get_session()
    user = session.query(UserModel).filter_by(email=email).first()
    if not user:
        return None
    return user


def get_user_by_id(user_id: UUID) -> type[UserModel] | None:
    """
    Retrieve a user by their unique ID.

    Args:
        user_id (UUID): The unique identifier of the user.

    Returns:
        UserModel | None: The user if found, otherwise None.
    """
    session = get_session()
    print(f" ====={type(UserModel.id)}, {type(user_id)}")
    user = session.query(UserModel).filter_by(id=user_id).first()
    print(user.id)
    if not user:
        return None
    return user


def update_user(user_id: UUID, user_data: dict) -> type[UserModel] | None:
    """
    Update a user's details.

    Args:
        user_id (UUID): The unique identifier of the user to update.
        user_data (dict): A dictionary containing updated user details.

    Returns:
        UserModel | None: The updated user if found, otherwise None.
    """
    session = get_session()
    user = session.query(UserModel).filter_by(id=user_id).first()
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    user.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)
    return user


def update_user_password(hashed_password_update,
                         user_id: UUID | None = None, username: str | None = None
                         ) -> type[UserModel] | None:
    """
    Update a user's password.

    Args:
        hashed_password_update: The new hashed password.
        user_id (UUID | None): The unique identifier of the user (optional).
        username (str | None): The username of the user (optional).

    Returns:
        UserModel | None: The updated user if found, otherwise None.
    """
    session = get_session()
    user = session.query(UserModel).filter(
        (UserModel.id == user_id) | (UserModel.username == username)
    ).first()
    if not user:
        return None
    user.hashed_password = hashed_password_update
    user.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)
    return user


def update_login_time(user_id: UUID):
    """
    Update the last login time of a user.

    Args:
        user_id (UUID): The unique identifier of the user.

    Returns:
        UserModel: The user with the updated login time.
    """
    session = get_session()
    user = session.query(UserModel).filter_by(id=user_id).first()
    user.last_login_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)
    return user
