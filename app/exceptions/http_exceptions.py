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

ORGANIZATION_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Organization not found."
)

# Organization Member Related Exception
ORGANIZATION_MEMBER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found in the organization."
)

ORGANIZATION_ALREADY_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Organization with same name already exists."
)

ALREADY_MEMBER_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User is already a member of the organization."
)


# Permission Related Exception
FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to perform this action."
)

PERMISSION_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Organization associated to current user not found."
)


# Role Related Exception
ROLE_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Given role not found."
)
