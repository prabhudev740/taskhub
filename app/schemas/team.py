""" The Team Schema """

from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field


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
