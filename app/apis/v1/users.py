""" User Related APIs """

from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Path
from core.dependencies import CurrentActiveUserDep
from core.logging_conf import Logging
from schemas.user import User, UpdateUser, UserPasswordUpdate, UserProfile, UserMessageResponse
from services.user_service import update_current_active_user, get_user_profile_by_id, \
    update_current_active_user_password


log = Logging(__name__).log()

router = APIRouter(
    prefix="/api/v1",
    dependencies=[],
    tags=['users'],
    responses={404: {"message": "Page Not Found!"}}
)


@router.get("/users/me", response_model=User)
async def get_current_user(current_user: CurrentActiveUserDep):
    """ Retrieve current user's details. """
    return current_user


@router.put("/users/me", response_model=User)
async def update_current_user(current_user: CurrentActiveUserDep, update_user: UpdateUser):
    """ Update current user's data. """
    return await update_current_active_user(current_user.id, update_user)


@router.patch("/users/me/password", response_model=UserMessageResponse)
async def update_current_user_password(current_user: CurrentActiveUserDep,
                                       update_password: UserPasswordUpdate):
    """ Reset current user's password. """
    return await update_current_active_user_password(current_user.email, update_password)


@router.get("/users/me/settings")
async def get_current_user_settings():
    """ Retrieve current user's settings. """
    ...

@router.put("/users/me/settings")
async def update_current_user_settings():
    """ Update current user settings. """
    ...


@router.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(current_user: CurrentActiveUserDep,
                           user_id: Annotated[str, Path(...)]):
    """ Retrieve user's profile by user id. """
    log.info("current_user: %s", current_user.username)
    return await get_user_profile_by_id(user_id=UUID(user_id))
