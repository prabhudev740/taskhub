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


class Role(BaseModel):
    """
    Represents schema for role.

    Attributes:
        id (UUID): The ID of the Role.
        name (str): The name of the role.
        description (str): Description fot the role.
        organization_id (UUID): The ID of the organization.
        is_system_role (bool): True if system role, else False
    """
    id: UUID
    name: str
    description: str
    is_system_role: bool
    organization_id: UUID


class Permission(BaseModel):
    """
    Permission schema for validation.

    Attributes:
        id (UUID): The ID of the organization.
        name (str): The name of the organization.
        description (str): The description of the organization.
    """
    id: UUID
    name: str
    description: str | None

# Request Schema
class CreateRole(BaseModel):
    """
    Schema for creating a new role.

    Attributes:
        name (str): Name of the role. Must have a minimum length of 3 characters.
        description (str | None): Optional description of the role.
        is_system_role (bool): Indicates if the role is a system role. Defaults to False.
        organization_id (UUID | None): Optional ID of the organization associated with the role.
        team_id (UUID | None): Optional ID of the team associated with the role.
    """
    name: Annotated[str, Field(min_length=3)]
    description: Annotated[str | None, Field()] = None
    is_system_role: Annotated[bool, Field()] = False
    organization_id: Annotated[UUID | None, Field()] = None
    team_id: Annotated[UUID | None, Field()] = None


class CreateCustomRole(BaseModel):
    """
    Request schema for creating custom roles.

    Attributes:
        name (str): Name of the new role (min_length=5, max_length=64)
        description (str): Description for new role.
        permission_ids (list[UUID]): The list of permission ID.
    """
    name: Annotated[str, Field(min_length=5, max_length=64)]
    description: Annotated[str | None, Field(default=None)]
    permission_ids: Annotated[list[UUID], Field()]


# Response Schema
class RoleResponse(BaseModel):
    """
    Response schema for organization role.

    Attributes:
        id (UUID): The ID of the Role.
        name (str): The name of the role.
        description (str): Description fot the role.
        organization_id (UUID): The ID of the organization.
        is_system_role (bool): True if system role, else False
        permissions (list[Permission]): List ot Permission model
    """
    id: UUID
    name: str
    description: str | None
    organization_id: UUID
    is_system_role: bool
    permissions: list[Permission]


class AllRoleResponse(BaseModel):
    """
    Response schema for roles in an organization.

    Attributes:
        items (list[RoleResponse]): The list of roles in the organization.
    """
    items: list[RoleResponse]


class PermissionsResponse(BaseModel):
    """
    Response schema for all permission in an organization.

    Attributes:
        items (list[Permission]): List of all the Permissions.
        total (int): Count of permission defined in the organization.
    """
    items: list[Permission]
    total: int
