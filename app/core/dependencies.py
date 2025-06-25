""" Dependencies """

from typing import Annotated
from fastapi import Depends
from schemas.user import User
from services.user_service import get_current_active_user


# Dependency for retrieving the current active user
CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]
