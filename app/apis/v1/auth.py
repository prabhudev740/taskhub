from datetime import timedelta, datetime
from uuid import UUID

from fastapi import APIRouter, Query, HTTPException, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.logging_conf import Logging
from core.security import  get_hashed_password
from db.crud.crud_user import create_user
from schemas.token import Token
from schemas.user import User, CreateUser
from services.auth_service import authenticate_user, create_access_token
from services.user_service import create_new_user

log = Logging(__name__).log()

router = APIRouter(
    prefix="/api/v1/auth",
    dependencies=[],
    responses={404: {"message": "Page Not Found!"}},
    tags=['auth']
)


@router.post("/token")
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expire_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", expires_in=60)

@router.post("/refresh")
async def refresh_token():
    return {"message": "/refresh"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: Annotated[User, Depends(create_new_user)]) -> User:
    return user

@router.post("/logout")
async def logout_user():
    return {"message": "/logout"}

@router.post("/request-password-reset")
async def request_password_reset(email):
    return {"message": "/request-password-reset"}

@router.post("/password-reset")
async def password_reset():
    return {"message": "/password-reset"}


@router.get("/password-policy")
async def password_policy():
    return {"message": "/password-policy"}
