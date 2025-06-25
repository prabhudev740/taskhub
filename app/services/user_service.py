""" User Service """

from uuid import UUID
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from core.config import SECRET_KEY, ALGORITHM
from core.logging_conf import Logging
from core.security import oauth2_scheme, get_hashed_password, verify_hash_password
from db.crud.crud_user import get_user_by_username, create_user, update_user_password, \
    update_user, get_user_by_id, get_user_by_email
from exceptions import http_exceptions
from schemas.token import TokenData
from schemas.user import User, CreateUser, UpdateUser, UserPasswordUpdate, UserProfile, \
    UserMessageResponse


# Initialize logging for the module
log = Logging(__name__).log()

def is_active_user(is_active: bool):
    """
    Check if the user is active.

    Args:
        is_active (bool): Indicates whether the user is active.

    Raises:
        HTTPException: If the user is inactive.
    """
    if not is_active:
        raise HTTPException(status_code=403, detail="Inactive User")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The authentication token.

    Returns:
        User: The user object corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        log.info("%s", payload)
        username = payload.get('sub')
        if not username:
            raise http_exceptions.CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
        user = get_user_by_username(username=token_data.username)
        if not user:
            raise http_exceptions.USER_NOT_FOUND_EXCEPTION
        response_user = User.model_validate(user)
        return response_user
    except InvalidTokenError as exc:
        raise http_exceptions.CREDENTIALS_EXCEPTION from exc

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retrieve the current active user.

    Args:
        current_user (User): The current user object.

    Returns:
        User: The active user object.

    Raises:
        HTTPException: If the user is inactive.
    """
    is_active_user(current_user.is_active)
    return current_user

async def create_new_user(create_data: CreateUser, is_superuser: bool = False) -> User:
    """
    Create/Register a new user.

    Args:
        create_data (CreateUser): The data required to create a new user.
        is_superuser (bool, optional): Indicates if the user is a superuser. Defaults to False.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException: If the username or email already exists.
    """
    if get_user_by_username(create_data.username):
        raise http_exceptions.USERNAME_ALREADY_EXITS_EXCEPTION
    if get_user_by_email(create_data.email):
        raise http_exceptions.EMAIL_ALREADY_EXITS_EXCEPTION
    hashed_password = get_hashed_password(create_data.password)
    user_data = create_data.model_dump(exclude_unset=True)
    user_data.pop("password", None)  # Remove plain password
    user_data.update({"hashed_password": hashed_password})
    if is_superuser:
        user_data.update({"is_superuser": True})

    user = create_user(user_data)
    user_response = User.model_validate(user)
    return user_response

async def update_current_active_user(current_user_id: UUID, user_update: UpdateUser):
    """
    Update the details of the current user.

    Args:
        current_user_id (UUID): The ID of the current user.
        user_update (UpdateUser): The fields to update for the user.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: If the user is not found.
    """
    user_data = user_update.model_dump(exclude_unset=True)
    user = update_user(current_user_id, user_data)
    if not user:
        raise http_exceptions.USER_NOT_FOUND_EXCEPTION
    user_response = User.model_validate(user)
    return user_response

async def update_current_active_user_password(
        username: str,
        user_password: UserPasswordUpdate) -> UserMessageResponse:
    """
    Update the current user's password.

    Args:
        username (str): The username of the user.
        user_password (UserPasswordUpdate): The password update details.

    Returns:
        UserMessageResponse: A message indicating the password update status.

    Raises:
        HTTPException: If the user is not found, the current password is incorrect,
        or the new passwords do not match.
    """
    user = get_user_by_username(username=username)
    if not user:
        raise http_exceptions.USER_NOT_FOUND_EXCEPTION
    if not verify_hash_password(user_password.password, user.hashed_password):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Current password is incorrect."
    )
    if user_password.new_password != user_password.confirm_new_password:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="New passwords do not match."
    )
    log.debug("user id: %s, type: %s", user.id, type(user.id))
    hashed_password_update = get_hashed_password(user_password.new_password)
    update_user_password(hashed_password_update, user_id=user.id)
    return UserMessageResponse(message = "Password updated successfully.")

async def get_user_profile_by_id(user_id: UUID) -> UserProfile:
    """
    Retrieve the user's profile by user ID.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        UserProfile: The user's profile object.

    Raises:
        HTTPException: If the user is not found.
    """
    user = get_user_by_id(user_id)
    if not user:
        raise http_exceptions.USER_NOT_FOUND_EXCEPTION
    user_response = UserProfile.model_validate(user)
    return user_response
