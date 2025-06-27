from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID
from datetime import datetime
from schemas.user import UserProfileShort


class Organization(BaseModel):
    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CreateOrganization(BaseModel):
    name: Annotated[str, Field(min_length=5, max_length=32)]
    description: Annotated[str | None,  Field(max_length=1024)]


class UpdateOrganization(BaseModel):
    name: Annotated[str | None, Field(min_length=5, max_length=32)] | None
    description: Annotated[str | None,  Field(max_length=1024)] = None
    owner_id: Annotated[UUID | None, Field()] = None

    model_config = {"from_attributes": True}



class OrganizationUserRole(BaseModel):
    username: Annotated[str, Field(min_length=5)]
    role_name: Annotated[str | None, Field(min_length=2, default="Viewer")]


class AddOrganizationMembersRequest(BaseModel):
    user_roles: list[OrganizationUserRole]


class AddOrganizationMemberResponse(BaseModel):
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
    items: list[Organization]
    total: int
    page: int
    size: int
    pages: int


class OrganizationByIDResponse(Organization):
    owner_details: UserProfileShort
    member_count: int


class OrganizationMessageResponse(BaseModel):
    message: str

