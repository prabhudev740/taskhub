""" Define all HTTP Exceptions. """
from fastapi import status, HTTPException


# Authentication Exceptions
INVALID_USERNAME_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password. Please check your credentials and try again.",
    headers={"WWW-Authenticate": "Bearer"}
)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# User Related Exceptions
USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found."
)

USERNAME_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User with given username not found"
)

EMAIL_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User with given email not found"
)

USERNAME_ALREADY_EXITS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exits."
)

EMAIL_ALREADY_EXITS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already exits."
)


# Organization Related Exception


# Organization Member Related Exception
ORGANIZATION_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Organization not found."
)

ALREADY_MEMBER_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User is already a member of the organization."
)

# Permission Related Exception


# Role Related Exception
ROLE_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Given role not found."
)
