import jwt

from fastapi import Depends, HTTPException, status

from core.config import SECRET_KEY, ALGORITHM
from core.logging_conf import Logging
from core.security import oauth2_scheme
from db.crud.crud_user import get_user_by_username
from schemas.token import TokenData
from schemas.user import User
from typing import Annotated
from jwt.exceptions import InvalidTokenError

log = Logging(__name__).log()

def is_active_user(is_active: bool):
    if not is_active:
        raise HTTPException(status_code=403, detail="Inactive User")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        log.info(f"{payload}")
        username = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = get_user_by_username(email=token_data.username)
    except InvalidTokenError:
        raise credentials_exception
    response_user = User.model_validate(user)
    return response_user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    is_active_user(current_user.is_active)
    return current_user

