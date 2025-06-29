""" ORG schema """
from typing import Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from schemas.role import RoleShort
from schemas.user import UserProfileShort


class Organization(BaseModel):
    """
    Represents an organization entity.

    Attributes:
        id (UUID): Unique identifier for the organization.
        name (str): Name of the organization.
        description (str): Description of the organization.
        owner_id (UUID): Unique identifier of the owner of the organization.
        created_at (datetime): Timestamp when the organization was created.
    """
    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CreateOrganization(BaseModel):
    """
    Request schema for creating a new organization.

    Attributes:
        name (Annotated[str, Field]): Name of the organization
        (minimum length: 5, maximum length: 32).
        description (Annotated[str | None, Field]): Description of the organization
        (optional, maximum length: 1024).
    """
    name: Annotated[str, Field(min_length=5, max_length=32)]
    description: Annotated[str | None, Field(max_length=1024)]


class UpdateOrganization(BaseModel):
    """
    Request schema for updating an organization.

    Attributes:
        name (Annotated[str | None, Field] | None): Updated name of the organization
        (optional, minimum length: 5, maximum length: 32).
        description (Annotated[str | None, Field]): Updated description of the organization
        (optional, maximum length: 1024).
        owner_id (Annotated[UUID | None, Field]): Updated owner ID of the organization (optional).
    """
    name: Annotated[str | None, Field(min_length=5, max_length=32)] | None
    description: Annotated[str | None, Field(max_length=1024)] = None
    owner_id: Annotated[UUID | None, Field()] = None

    model_config = {"from_attributes": True}


class OrganizationUserRole(BaseModel):
    """
    Represents a user's role within an organization.

    Attributes:
        username (Annotated[str, Field]): Username of the user (minimum length: 5).
        role_name (Annotated[str | None, Field]): Name of the role assigned to the user
        (optional, minimum length: 2, default: "Viewer").
    """
    username: Annotated[str, Field(min_length=5)]
    role_name: Annotated[str | None, Field(min_length=2, default="Viewer")]


class AddOrganizationMembersRequest(BaseModel):
    """
    Request schema for adding members to an organization.

    Attributes:
        user_roles (list[OrganizationUserRole]): List of user roles to be added to the organization.
    """
    user_roles: list[OrganizationUserRole]


class UpdateOrganizationMemberRole(BaseModel):
    """
    Request schema for updating a role for organization member.

    Attributes:
        role_id (UUID): Unique identifier of the role to be assigned.
    """
    role_id: Annotated[UUID, Field()]


# Response
class OrganizationMemberResponse(BaseModel):
    """
    Response schema for adding a member to an organization.

    Attributes:
        user_id (UUID): Unique identifier of the user.
        organization_id (UUID): Unique identifier of the organization.
        role_id (UUID): Unique identifier of the role assigned to the user.
        role_name (str): Name of the role assigned to the user.
        user_email (str): Email address of the user.
        user_full_name (str): Full name of the user.
        status (str): Status of the membership addition.
        joined_at (datetime): Timestamp when the user joined the organization.
    """
    user_id: UUID
    organization_id: UUID
    role_id: UUID
    role_name: str
    user_email: str
    user_full_name: str
    status: str
    joined_at: datetime

    model_config = {"from_attributes": True}


class OrganizationResponse(BaseModel):
    """
    Response schema for paginated organization data.

    Attributes:
        items (list[Organization]): List of organizations.
        total (int): Total number of organizations.
        page (int): Current page number.
        size (int): Number of items per page.
        pages (int): Total number of pages.
    """
    items: list[Organization]
    total: int
    page: int
    size: int
    pages: int


class OrganizationByIDResponse(Organization):
    """
    Response schema for organization details by ID.

    Attributes:
        owner_details (UserProfileShort): Details of the organization owner.
        member_count (int): Number of members in the organization.
    """
    owner_details: UserProfileShort
    member_count: int


class OrganizationMemberData(BaseModel):
    """
    Represents data for a member of an organization.

    Attributes:
        user (UserProfileShort): Profile details of the user.
        role (RoleShort): Role details of the user within the organization.
        joined_at (datetime): Timestamp when the user joined the organization.
    """
    user: UserProfileShort
    role: RoleShort
    joined_at: datetime


class OrganizationMembersResponse(BaseModel):
    """
    Response schema for members of an organization.

    Attributes:
        items (list[OrganizationMemberData]): List of organization members' data.
        total (int): Total number of members.
        page (int): Current page number.
        size (int): Number of items per page.
        pages (int): Total number of pages.
    """
    items: list[OrganizationMemberData]
    total: int
    page: int
    size: int
    pages: int
