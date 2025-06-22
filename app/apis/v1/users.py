from uuid import UUID
from fastapi import APIRouter, Path
from typing import Annotated
from core.logging_conf import Logging
from schemas.user import User, UpdateUser, UserPasswordUpdate, UserProfile, UserMessageResponse
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
    return await update_current_active_user(current_user.id, update_user)

@router.patch("/users/me/password", response_model=UserMessageResponse)
async def update_current_user_password(current_user: CurrentActiveUserDep,
                                       update_password: UserPasswordUpdate):
    return await update_current_active_user_password(current_user.email, update_password)

@router.get("/users/me/settings")
async def get_current_user_settings():
    ...

@router.put("/users/me/settings")
async def update_current_user_settings():
    ...

@router.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(current_user: CurrentActiveUserDep,
                           user_id: Annotated[str, Path(...)]) -> UserProfile:
    return await get_user_profile_by_id(user_id=UUID(user_id))
