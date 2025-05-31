from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from core.logging_conf import Logging
from schemas.user import User
from services.user_service import get_current_active_user

router = APIRouter(prefix="/api/v1", tags=['users'])
log = Logging(__name__).log()

login = True

@router.get("/users/me")
async def get_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    log.info(f"{current_user}")
    # if not login:
    #     log.debug("Not logged in")
    #     raise HTTPException(status_code=404, detail="Not logged in")
    return current_user

@router.put("/users/me")
async def update_current_user():
    return {"message": "me"}

@router.patch("/users/me/password")
async def update_current_user_password():
    return {"message": "me"}

@router.get("/users/me/settings")
async def get_current_user_settings():
    pass

@router.put("/users/me/settings")
async def get_current_user_settings():
    pass

@router.get("/users/{user_id}/profile")
async def get_current_user_settings():
    pass
