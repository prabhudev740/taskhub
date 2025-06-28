""" Schemas for roles """

from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field

# Internal Schema
class RoleShort(BaseModel):
    """
    Represents a short version of a role with minimal details.

    Attributes:
        id (UUID): Unique identifier for the role.
        name (str): Name of the role.
    """
    id: UUID
    name: str

# Request Schema
class CreateRoleRequest(BaseModel):
    """
    Schema for creating a new role.

    Attributes:
        name (str): Name of the role. Must have a minimum length of 3 characters.
        description (str | None): Optional description of the role.
        is_system_role (bool): Indicates if the role is a system role. Defaults to False.
        organization_id (UUID | None): Optional ID of the organization associated with the role.
    """
    name: Annotated[str, Field(min_length=3)]
    description: Annotated[str | None, Field()] = None
    is_system_role: Annotated[bool, Field()] = False
    organization_id: Annotated[UUID | None, Field()] = None

# Response Schema
# (No response schema defined yet)
