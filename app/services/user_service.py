from uuid import UUID

import jwt

from fastapi import Depends, HTTPException, status

from core.config import SECRET_KEY, ALGORITHM
from core.logging_conf import Logging
from core.security import oauth2_scheme, get_hashed_password
from db.crud.crud_user import get_user_by_username, create_user, update_user
from schemas.token import TokenData
from schemas.user import User, CreateUser, UpdateUser
from typing import Annotated
from jwt.exceptions import InvalidTokenError

log = Logging(__name__).log()

def is_active_user(is_active: bool):
    if not is_active:
        raise HTTPException(status_code=403, detail="Inactive User")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found. Unable to update user information."
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        log.info(f"{payload}")
        username = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = get_user_by_username(email=token_data.username)
        if not user:
            raise user_not_found_exception
        response_user = User.model_validate(user)
        return response_user
    except InvalidTokenError:
        raise credentials_exception


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    is_active_user(current_user.is_active)
    return current_user


async def create_new_user(create_data: CreateUser) -> User:
    conflict_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="An account with the provided email already exists.",
    )

    is_exists = get_user_by_username(create_data.email)
    if is_exists:
        raise conflict_exception
    hashed_password = get_hashed_password(create_data.password)
    user_data = create_data.model_dump(exclude_unset=True)
    user_data.pop("password", None)  # Remove plain password
    user_data.update({"hashed_password": hashed_password})
    log.info(f"{user_data}")

    user = create_user(user_data)
    user_response = User.model_validate(user)
    return user_response


async def update_current_active_user(current_user_id: UUID, user_update: UpdateUser):
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found. Unable to update user information."
    )
    user_data = user_update.model_dump(exclude_unset=True)
    user = update_user(current_user_id, user_data)
    if not user:
        raise user_not_found_exception
    user_response = User.model_validate(user)
    return user_response