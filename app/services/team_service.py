""" Team Services. """

from  pprint import pprint
from uuid import UUID
from core.logging_conf import Logging
from core.permission_config import TEAM_ROLES
from db.crud.crud_organization import create_organization_team
from db.crud.crud_team import get_team_by_name, create_team, get_member_count_by_team_id, \
    get_organization_teams, create_team_member
from db.crud.curd_role import get_role_by_role_name_team_id, create_role
from db.models import TeamModel
from exceptions import http_exceptions
from schemas.role import CreateRole
from schemas.team import CreateTeam, SingleTeamResponse, AllTeamResponse
from services.organization_service import map_role_permissions


log = Logging(__name__).log()


async def create_default_team_role_permissions(team_id: UUID):
    """
    Create Default roles and permissions the for the team.

    Args:
        team_id (UUID): The ID of the team.
    """
    # Create roles and assign permissions only if role not present
    for role_data in TEAM_ROLES.values():
        if not get_role_by_role_name_team_id(role_data['name'], team_id=team_id):
            role = CreateRole(name=role_data['name'], description=role_data['description'],
                              team_id=team_id)
            role = role.model_dump(exclude_unset=True)
            created_role = create_role(role)
            role_id = created_role.id
            await map_role_permissions(role_id, role_data['permissions'])



async def add_new_team_member(current_user_id: UUID, team_id: UUID, role_name: str):
    """
    Add a new member to a team.

    Args:
        current_user_id (UUID): The ID of the current user.
        team_id (UUID): The ID of the team.
        role_name (str): The name of the role to assign to the user.

    Returns:
        dict: The updated team member data.

    Raises:
        HTTPException: If the specified role is not found.
    """
    log.info("Checking if the role %s exists before creating.", role_name)
    role = get_role_by_role_name_team_id(role_name=role_name, team_id=team_id)
    if not role:
        log.warning("Could not find the role with role name %s", role_name)
        raise http_exceptions.ROLE_NOT_FOUND_EXCEPTION

    log.info("Create the team members.")
    team_member = {"user_id": current_user_id, "team_id": team_id, "role_id": role.id}
    return create_team_member(team_member)


async def get_single_team_response(team: TeamModel) -> SingleTeamResponse:
    """
    Generate the single team response from the TeamModel object with member count.
    TODO: We can further add assigned projects in Response

    Args:
        team (TeamModel): SQLAlchemy model retrieved from db.

    Returns:
        SingleTeamResponse: The response of created team.
    """
    log.info("Retrieve the count of member of team: %s", team.name)
    member_count = get_member_count_by_team_id(team_id=team.id)
    log.debug("Number of members in team %s is %s", team.name, member_count)
    team.member_count = member_count
    return SingleTeamResponse.model_validate(team)


async def add_new_team_in_organization(org_id: UUID, user_id: UUID, role_name: str,
                                       team: CreateTeam, is_owner: bool = False
                                       ) -> SingleTeamResponse:
    """
    Create a new team for given organization_id.

    Args:
        org_id (UUID): The ID of the organization.
        user_id (UUID): The ID of the current user.
        role_name (str): The name of the role.
        team (CreateTeam): The team to be created.
        is_owner (bool): True if the owner, False otherwise.

    Raises:
        HTTPException: When team name already exists.

    Returns:
        SingleTeamResponse: The response of created team.
    """
    log.info("Checking if team name '%s' exists in organization '%s'", team.name, org_id)
    existing_team = get_team_by_name(team_name=team.name, org_id=org_id)
    if existing_team:
        log.warning("Team name '%s' already exists in organization '%s'", team.name, org_id)
        raise http_exceptions.TEAM_ALREADY_EXISTS_EXCEPTION

    log.info("Converting team data for creation")
    team_data = team.model_dump(exclude_unset=True)
    team_data['organization_id'] = org_id
    if is_owner:
        team_data['owner_id'] = user_id
    log.debug("Team to be created: %s", pprint(team_data))

    log.info("Creating new team '%s' in organization '%s'", team.name, org_id)
    created_team = create_team(team_data=team_data)
    log.debug("Created Team: %s", created_team)

    log.info("Updating the organization team relation.")
    organization_team = \
        {"organization_id": created_team.organization_id, "team_id": created_team.id}
    create_organization_team(organization_team=organization_team)

    log.info("Creating default role permissions for the team")
    await create_default_team_role_permissions(team_id=created_team.id)

    log.info("Updating the team member relation.")
    await add_new_team_member(current_user_id=user_id, team_id=created_team.id,
                              role_name=role_name)
    return await get_single_team_response(team=created_team)


async def retrieve_all_team_of_the_organization(organization_id: UUID,  page: int, size: int,
                                                sort_by: str) -> AllTeamResponse:
    """
    Retrieve the list tams of the specific organization.

    Args:
        organization_id (str): ID of the organization.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        sort_by (str): Field to sort the organizations by.

    Returns:
        AllTeamResponse: List of all the teams.
    """
    log.info("Retrieve organization team for organization: %s", organization_id)
    sorted_teams, total, pages = get_organization_teams(organization_id=organization_id, page=page,
                                      size=size, sort_by=sort_by)

    response_team = \
        {"items": sorted_teams, "total": total, "page": page, "size": size, "pages": pages}
    teams_with_count = []
    for team in sorted_teams:
        team_dict = team.__dict__.copy()
        team_dict["member_count"] = get_member_count_by_team_id(team.id)
        teams_with_count.append(team_dict)

    response_team.update({"items": teams_with_count})
    return AllTeamResponse.model_validate(response_team)
