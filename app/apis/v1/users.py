""" User Related APIs """

from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Path
from core.dependencies import CurrentActiveUserDep
from core.logging_conf import Logging
from schemas.user import User, UpdateUser, UserPasswordUpdate, UserProfile, UserMessageResponse
from services.user_service import update_current_active_user, get_user_profile_by_id, \
    update_current_active_user_password


# Initialize logger
log = Logging(__name__).log()


# Create an API router for user-related endpoints
router = APIRouter(
    prefix="/api/v1",  # Base path for all routes
    dependencies=[],  # Dependencies for all routes
    tags=['users'],  # Tag for grouping routes in documentation
    responses={404: {"message": "Page Not Found!"}}  # Default response for 404 errors
)


@router.get("/users/me", response_model=User)
async def get_current_user(current_user: CurrentActiveUserDep):
    """
    Retrieve current user's details.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.

    Returns:
        User: The details of the current user.
    """
    return current_user


@router.put("/users/me", response_model=User)
async def update_current_user(current_user: CurrentActiveUserDep, update_user: UpdateUser):
    """
    Update current user's data.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        update_user (UpdateUser): Data to update the user's information.

    Returns:
        User: The updated user details.
    """
    return await update_current_active_user(current_user.id, update_user)


@router.patch("/users/me/password", response_model=UserMessageResponse)
async def update_current_user_password(current_user: CurrentActiveUserDep,
                                       update_password: UserPasswordUpdate):
    """
    Reset current user's password.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        update_password (UserPasswordUpdate): New password details.

    Returns:
        UserMessageResponse: Response message indicating the result of the password update.
    """
    return await update_current_active_user_password(current_user.email, update_password)


@router.get("/users/me/settings")
async def get_current_user_settings():
    """
    Retrieve current user's settings.

    Returns:
        Any: The user's settings (to be implemented).
    """


@router.put("/users/me/settings")
async def update_current_user_settings():
    """
    Update current user's settings.

    Returns:
        Any: The updated settings (to be implemented).
    """


@router.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(current_user: CurrentActiveUserDep,
                           user_id: Annotated[str, Path(...)]):
    """
    Retrieve user's profile by user ID.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        user_id (str): The ID of the user whose profile is being retrieved.

    Returns:
        UserProfile: The profile of the specified user.
    """
    log.info("current_user: %s", current_user.username)
    return await get_user_profile_by_id(user_id=UUID(user_id))
