import jwt

from fastapi import Depends, HTTPException, status

from core.config import SECRET_KEY, ALGORITHM
from core.logging_conf import Logging
from core.security import oauth2_scheme, get_user, fake_users_db
from schemas.token import TokenData
from schemas.user import User
from typing import Annotated
from jwt.exceptions import InvalidTokenError

log = Logging(__name__).log()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
        user = get_user(fake_users_db, username=token_data.username)
    except InvalidTokenError:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user