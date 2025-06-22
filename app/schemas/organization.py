from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID
from datetime import datetime


class Organization(BaseModel):
    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class OrganizationResponse(BaseModel):
    items: list[Organization]
    total: int
    page: int
    size: int
    pages: int


class CreateOrganization(BaseModel):
    name: Annotated[str, Field(min_length=5, max_length=32)]
    description: Annotated[str | None,  Field(max_length=1024)]


class OrganizationUserRole(BaseModel):
    username: Annotated[str, Field(min_length=5)]
    role: Annotated[str | None, Field(min_length=2, default="Viewer")]


class AddOrganizationMembersRequest(BaseModel):
    user_roles: list[OrganizationUserRole]


class AddOrganizationMemberResponse(BaseModel):
  user_id: UUID
  organization_id: UUID
  role_id: UUID
  role_name: str
  user_email: str
  user_full_name: str
  status: bool
  joined_at: datetime

  model_config = {"from_attributes": True}

