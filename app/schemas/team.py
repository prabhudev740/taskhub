""" The Team Schema """

from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field
from schemas.user import UserProfileShort


# Internal Schema
class Team(BaseModel):
    """
    The Schema for Team.

    Attributes:
        id (UUID): The ID of thr team.
        name (str): The name of the Team.
        description (str): The description of the team.
    """
    id: UUID
    name: str
    description: str


# Request Schema
class CreateTeam(BaseModel):
    """
     Request schema for create team.

    Attributes:
        name (str): The name of the Team.
        description (str): The description of the team.
    """
    name: Annotated[str, Field(min_length=3, max_length=64)]
    description: Annotated[str | None, Field(default=None)]


class UpdateTeam(BaseModel):
    """
     Request schema for update team.

    Attributes:
        name (str): The name of the Team.
        description (str): The description of the team.
    """
    name: Annotated[str, Field(min_length=3, max_length=64, default=None)]
    description: Annotated[str | None, Field(default=None)]


class AddTeamMember(BaseModel):
    """
    Base schema for adding a team member.

    Attributes:
        user_id (UUID): The ID of the user.
        role_name (str): The name of the role.
    """
    user_id: Annotated[UUID, Field()]
    role_name: Annotated[str | None, Field(min_length=2, default="Viewer")]


class AddTeamMembersRequest(BaseModel):
    """
    The schema for adding multiple team members.

    Attributes:
         users (list[AddTeamMember]):  The list of member roles to be added.
    """
    users: list[AddTeamMember]


# Response Schema
class SingleTeamResponse(BaseModel):
    """
    Response schema for a team.

    Attributes:
        id (UUID): The ID of thr team.
        name (str): The name of the Team.
        description (str): The description of the team.
        organization_id (UUID): The ID of the organization of the team.
        created_at (datetime): The Timezone when the team is created.
        updated_at (datetime): The Timezone when the team is updated.
        member_count (int): The count of members in the team.
    """
    id: UUID
    name: str
    description: str
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
    member_count: int

    model_config = {"from_attributes": True}


class AllTeamResponse(BaseModel):
    """
    The response model for all teams.

    Args:
        items (list[SingleTeamResponse]): The list of all the teams.
        total (int): Total number of teams.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        pages (int): Total number of pages.
    """
    items: list[SingleTeamResponse]
    total: int
    page: int
    size: int
    pages: int


class AddMemberResponse(BaseModel):
    """
    Response schema for adding a team.

    Attributes:
        team_id (UUID): The ID of the team.
        organization_id (UUID): The ID of the user.
        role_id (UUID): The ID of the role
        role_name (str): The name of the role.
        user_details (UserProfileShort): Schema for short user profile.
        added_at (datetime): Timestamp when the user added to the team.
    """
    team_id: UUID
    organization_id: UUID
    role_id: UUID
    role_name: str
    user_details: UserProfileShort
    added_at: datetime


class AllMembersResponse(BaseModel):
    """
    The response model for all teams members.

    Args:
        items (list[AddMemberResponse]): The list of all the team members.
        total (int): Total number of teams.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        pages (int): Total number of pages.
    """
    items: list[AddMemberResponse]
    total: int
    page: int
    size: int
    pages: int
