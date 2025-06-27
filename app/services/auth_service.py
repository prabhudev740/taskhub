""" Auth services """
from datetime import timedelta, datetime, timezone
import jwt
from core.config import SECRET_KEY, ALGORITHM
from core.security import verify_hash_password
from db.crud.crud_user import get_user_by_username, update_login_time
from fastapi import Request, HTTPException, status


def authenticate_user(username: str, password: str):
    """
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User | bool: The authenticated user object if successful, otherwise False.
    """
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_hash_password(password, user.hashed_password):
        return False
    update_login_time(user_id=user.id)
    return user

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    """
    Creates a JWT access token.

    Args:
        data (dict): The payload data to encode in the token.
        expire_delta (timedelta | None): The expiration time delta for the token (optional).

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token_from_cookies(request: Request) -> str:
    """
    Verifies the access token from cookies in the request.

    Args:
        request (Request): The FastAPI request object containing cookies.

    Returns:
        str: The access token retrieved from cookies.

    Raises:
        HTTPException: If the token is not found or invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(f"{request.cookies}")
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    return token
