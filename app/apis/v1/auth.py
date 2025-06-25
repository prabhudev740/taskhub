""" Auth APIs """

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.dependencies import CurrentActiveUserDep
from core.logging_conf import Logging
from exceptions import http_exceptions
from schemas.token import Token
from schemas.user import User, UserMessageResponse, CreateUser
from services.auth_service import authenticate_user, create_access_token
from services.user_service import create_new_user


# Initialize logger for the module
log = Logging(__name__).log()


# Create an API router for authentication-related endpoints
router = APIRouter(
    prefix="/api/v1/auth",  # Prefix for all routes in this router
    dependencies=[],  # Dependencies applied to all routes
    responses={404: {"message": "Page Not Found!"}},  # Default response for 404 errors
    tags=['auth']  # Tag for grouping routes in API documentation
)


@router.post("/token")
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Generate an access token for a user.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        Token: Access token details including token type and expiration time.

    Raises:
        HTTPException: If authentication fails due to invalid username or password.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise http_exceptions.INVALID_USERNAME_OR_PASSWORD

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username},
                                       expire_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", expires_in=60)


@router.post("/refresh")
async def refresh_token():
    """
    Refresh the access token.

    Returns:
        dict: Placeholder message for the refresh endpoint.
    """
    return {"message": "/refresh"}


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register_user(user: CreateUser):
    """
    Register a new user.

    Args:
        user (User): User details provided during registration.

    Returns:
        User: The newly created user object.
    """
    return await create_new_user(create_data=user)


@router.post("/logout", response_model=UserMessageResponse)
async def logout_user(current_user: CurrentActiveUserDep):
    """
    Log out the current user.

    Args:
        current_user (User): The currently authenticated user.

    Returns:
        UserMessageResponse: Confirmation message for successful logout.
    """
    log.info("Log out current user: %s", current_user.username)
    return UserMessageResponse(message="Logout Successful!")


@router.post("/request-password-reset")
async def request_password_reset():
    """
    Request a password reset.

    Returns:
        None: Placeholder for password reset request functionality.
    """
    ...


@router.post("/password-reset")
async def password_reset():
    """
    Reset the user's password.

    Returns:
        None: Placeholder for password reset functionality.
    """
    ...


@router.get("/password-policy")
async def password_policy():
    """
    Retrieve the password policy.

    Returns:
        None: Placeholder for password policy retrieval functionality.
    """
    ...
