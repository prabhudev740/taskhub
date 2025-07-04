""" Teams API """

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Path
from core.dependencies import CurrentActiveUserDep
from core.logging_conf import Logging
from schemas.team import CreateTeam, SingleTeamResponse
from services.organization_service import verify_current_user_role
from services.team_service import add_new_team_in_organization


log = Logging(__name__).log()
router = APIRouter(
    prefix="/api/v1/organization/{org_id}",
    tags=["teams"],
    dependencies=[],
    responses={404: {"message": "Page Not Found!"}}
)


@router.post("/teams", response_model=SingleTeamResponse)
async def create_new_team(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)],
                          new_team: CreateTeam):
    """
    Creates a new team within the specified organization.

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        org_id (str): The Organization ID for Path.
        new_team: The new team to be created.

    """
    log.info("%s", current_user)
    organization_id = UUID(org_id)
    await verify_current_user_role(user_id=current_user.id, org_id=organization_id,
                                   permission_names=['team:create'])
    return await add_new_team_in_organization(org_id=organization_id, team=new_team)


@router.get("teams")
def get_all_teams(current_user: CurrentActiveUserDep):
    """
    Retrieves a list of teams within the specified organization.
    """
    log.info("%s", current_user)


@router.get("/teams/{team_id}")
def get_specific_team(current_user: CurrentActiveUserDep):
    """
    Retrieves detailed information about a specific team.
    """
    log.info("%s", current_user)


@router.put("/teams/{team_id}")
def update_specific_team(current_user: CurrentActiveUserDep):
    """
    Updates a team's details. Requires appropriate permissions (e.g., org admin, team lead).
    """
    log.info("%s", current_user)


@router.delete("/teams/{team_id}")
def delete_specific_team(current_user: CurrentActiveUserDep):
    """
    Deletes a team. Requires appropriate permissions.
    """
    log.info("%s", current_user)


@router.post("/teams/{team_id}/members")
def add_a_member_to_team(current_user: CurrentActiveUserDep):
    """
    Adds a user (who must already be a member of the parent organization) to the specified
    team with a given role.
    """
    log.info("%s", current_user)


@router.get("/teams/{team_id}/members")
def retrieve_members_of_organization(current_user: CurrentActiveUserDep):
    """
    Retrieves a list of members for a specific team.
    """
    log.info("%s", current_user)


@router.put("/teams/{team_id}/members/{user_id}/role")
def update_user_role_in_team(current_user: CurrentActiveUserDep):
    """
    Updates the role of a specific member within a team.
    """
    log.info("%s", current_user)


@router.delete("/teams/{team_id}/members/{user_id}")
def remove_specific_member_from_team(current_user: CurrentActiveUserDep):
    """
    Removes a member from a team. They remain a member of the parent organization.
    """
    log.info("%s", current_user)
