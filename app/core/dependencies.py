""" Dependencies """

from typing import Annotated
from uuid import UUID
from fastapi import Depends
from schemas.user import User
from services.user_service import get_current_active_user
from utils.helpers import get_organization_id

# Dependency for retrieving the current active user
CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]
OrganizationIDDep = Annotated[UUID, Depends(get_organization_id)]
