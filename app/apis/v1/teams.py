""" Teams API """

from typing import Annotated
from fastapi import APIRouter, Query, status
from core.dependencies import CurrentActiveUserDep, OrganizationIDDep, TeamIDDep
from core.logging_conf import Logging
from schemas.team import CreateTeam, SingleTeamResponse, AllTeamResponse, UpdateTeam, \
    AddTeamMembersRequest, AddMemberResponse
from services.organization_service import verify_current_user_role
from services.team_service import add_new_team_in_organization, \
    retrieve_all_team_of_the_organization, get_team_by_team_id, update_team_details, \
    delete_the_team_by_id, add_team_members, verify_current_team_role

log = Logging(__name__).log()
router = APIRouter(
    prefix="/api/v1/organization/{organization_id}",
    tags=["teams"],
    dependencies=[],
    responses={404: {"message": "Page Not Found!"}}
)


@router.post("/teams", response_model=SingleTeamResponse)
async def create_new_team(current_user: CurrentActiveUserDep, organization_id: OrganizationIDDep,
                          new_team: CreateTeam):
    """
    Creates a new team within the specified organization.

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        organization_id (str): The Organization ID for Path.
        new_team: The new team to be created.

    Returns:
        SingleTeamResponse: The response after creating a team.
    """
    log.info("Verifying current user permission to create a team.")
    await verify_current_user_role(user_id=current_user.id, org_id=organization_id,
                                   permission_names=['team:create'])

    log.info("Creating a new team in the organization: %s", organization_id)
    return await add_new_team_in_organization(org_id=organization_id, user_id=current_user.id,
                                              role_name="Team Owner", team=new_team, is_owner=True)


@router.get("/teams", response_model=AllTeamResponse)
async def get_all_teams(current_user: CurrentActiveUserDep, organization_id: OrganizationIDDep,
                        page: Annotated[int, Query(ge=1)] = 1,
                        size: Annotated[int, Query(ge=10)] = 10,
                        sort_by: Annotated[str, Query()] = "name"):
    """
    Retrieves a list of teams within the specified organization.

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        organization_id (str): ID of the organization.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        sort_by (str): Field to sort the organizations by.

    Returns:
        AllTeamResponse: List of all the teams.
    """
    log.info("Verifying current user permission to read team.")
    await verify_current_user_role(org_id=organization_id, user_id=current_user.id,
                                   permission_names=['team:read'])

    log.info("Retrieving all teams in the organization: %s", organization_id)
    return await retrieve_all_team_of_the_organization(organization_id=organization_id, page=page,
                                                       size=size, sort_by=sort_by)


@router.get("/teams/{team_id}", response_model=SingleTeamResponse)
async def get_specific_team(current_user: CurrentActiveUserDep, organization_id: OrganizationIDDep,
                            team_id: TeamIDDep):
    """
    Retrieves detailed information about a specific team.

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        organization_id (UUID): ID of the organization.
        team_id (UUID): The ID of the team.

    Returns:
        SingleTeamResponse: The response after creating a team.
    """
    log.info("Verifying current user permission to read team.")
    await verify_current_user_role(org_id=organization_id, user_id=current_user.id,
                                   permission_names=['team:read'])

    log.info("Retrieving team details in the organization: %s for team: %s",
             organization_id, team_id)
    return await get_team_by_team_id(team_id=team_id)


@router.put("/teams/{team_id}", response_model=SingleTeamResponse)
async def update_specific_team(current_user: CurrentActiveUserDep,
                               organization_id: OrganizationIDDep, team_id: TeamIDDep,
                               team: UpdateTeam):
    """
    Updates a team's details. Requires appropriate permissions (e.g., org admin, team lead).

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        organization_id (OrganizationIDDep): ID of the organization.
        team_id (TeamIDDep): The ID of the team.
        team (UpdateTeam): Team details to be updated.

    Returns:
        SingleTeamResponse: The response after creating a team.
    """
    log.info("Verifying current user permission to update team.")
    await verify_current_user_role(user_id=current_user.id, org_id=organization_id,
                                   permission_names=['team:update'])

    log.info("Updating team details in the organization: %s for team: %s",
             organization_id, team_id)
    return await update_team_details(team_id=team_id, team_data=team)


@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specific_team(current_user: CurrentActiveUserDep,
                         organization_id: OrganizationIDDep, team_id: TeamIDDep):
    """
    Deletes a team. Requires appropriate permissions.

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        organization_id (OrganizationIDDep): ID of the organization.
        team_id (TeamIDDep): The ID of the team.
    """
    log.info("Verifying current user permission to update team.")
    await verify_current_user_role(user_id=current_user.id, org_id=organization_id,
                                   permission_names=['team:delete'])

    log.info("Deleting the team in the organization: %s for team: %s",
             organization_id, team_id)
    await delete_the_team_by_id(team_id=team_id)


@router.post("/teams/{team_id}/members", response_model=list[AddMemberResponse])
async def add_a_member_to_team(current_user: CurrentActiveUserDep, team_id: TeamIDDep,
                         organization_id: OrganizationIDDep, new_users: AddTeamMembersRequest):
    """
    Adds a user (who must already be a member of the parent organization) to the specified
    team with a given role.

    Args:
        current_user (CurrentActiveUserDep): The current active user.
        organization_id (OrganizationIDDep): ID of the organization.
        team_id (TeamIDDep): The ID of the team.
        new_users (AddTeamMembersRequest): List of user_id, role_ids.

    Returns:
        SingleMemberResponse: The response for added team member.
    """

    await verify_current_team_role(user_id=current_user.id, team_id=team_id,
                                   permission_names=['team:manage_members'])
    return await add_team_members(org_id=organization_id,
                                  team_id=team_id, user_roles=new_users)


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
