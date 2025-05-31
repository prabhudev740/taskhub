from datetime import timedelta

from fastapi import APIRouter, Query, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.logging_conf import Logging
from core.security import authenticate_user, create_access_token, fake_users_db
from schemas.token import Token

log = Logging(__name__).log()

router = APIRouter(
    prefix="/api/v1/auth",
    dependencies=[],
    responses={404: {"message": "Page Not Found!"}},
    tags=['auth']
)


@router.post("/token")
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expire_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", expires_in=60)

@router.post("/refresh")
async def refresh_token():
    return {"message": "/refresh"}

@router.post("/register")
async def register_user():
    return {"message": "/register"}

@router.post("/logout")
async def logout_user():
    return {"message": "/logout"}

@router.post("/request-password-reset")
async def request_password_reset():
    return {"message": "/request-password-reset"}

@router.post("/password-reset")
async def password_reset():
    return {"message": "/password-reset"}


@router.get("/password-policy")
async def password_policy():
    return {"message": "/password-policy"}
