from uuid import UUID
from fastapi import APIRouter, Path
from typing import Annotated
from core.logging_conf import Logging
from schemas.user import User, UpdateUser, UserPasswordUpdate, UserProfile
from services.user_service import update_current_active_user, get_user_profile_by_id, CurrentActiveUserDep, \
    update_current_active_user_password

router = APIRouter(prefix="/api/v1", tags=['users'])
log = Logging(__name__).log()


@router.get("/users/me", response_model=User)
async def get_current_user(current_user: CurrentActiveUserDep) -> User:
    log.info(f"{current_user}")
    return current_user

@router.put("/users/me", response_model=User)
async def update_current_user(current_user: CurrentActiveUserDep,
                              update_user: UpdateUser) -> User:
    user = await update_current_active_user(current_user.id, update_user)
    return user

@router.patch("/users/me/password")
async def update_current_user_password(current_user: CurrentActiveUserDep,
                                       update_password: UserPasswordUpdate):
    response = await update_current_active_user_password(current_user.email, update_password)
    return response

@router.get("/users/me/settings")
async def get_current_user_settings():
    ...

@router.put("/users/me/settings")
async def update_current_user_settings():
    ...

@router.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(current_user: CurrentActiveUserDep,
                           user_id: Annotated[str, Path(...)]) -> UserProfile:
    user_obj = UUID(user_id)
    user = await get_user_profile_by_id(user_obj)
    return user

