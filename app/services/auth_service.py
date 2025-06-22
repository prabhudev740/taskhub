from datetime import timedelta, datetime, timezone
import jwt
from core.config import SECRET_KEY, ALGORITHM
from core.security import verify_hash_password
from db.crud.crud_user import get_user_by_username, update_login_time
from fastapi import Request, HTTPException, status


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_hash_password(password, user.hashed_password):
        return False
    update_login_time(user_id=user.id)
    return user

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token_from_cookies(request: Request) -> str:
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
