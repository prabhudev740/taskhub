""" Team Services. """

from  pprint import pprint
from uuid import UUID
from core.logging_conf import Logging
from core.permission_config import TEAM_ROLES
from db.crud.crud_organization import create_organization_team
from db.crud.crud_team import get_team_by_name, create_team, get_member_count_by_team_id, \
    get_organization_teams, create_team_member, get_team_by_id, update_team, delete_team, \
    get_team_member_by_team_user_id
from db.crud.crud_user import get_user_by_id
from db.crud.curd_role import get_role_by_role_name_team_id, create_role
from db.models import TeamModel, TeamMemberModel
from exceptions import http_exceptions
from schemas.role import CreateRole
from schemas.team import CreateTeam, SingleTeamResponse, AllTeamResponse, UpdateTeam, \
    AddMemberResponse, AddTeamMembersRequest
from services.organization_service import map_role_permissions, get_verified_role_permissions


log = Logging(__name__).log()


async def verify_current_team_role(user_id: UUID, team_id: UUID, permission_names: list[str]):
    """
    Verify the current user's role and permissions in a team.

    Args:
        user_id (UUID): The ID of the user.
        team_id (UUID): The ID of the team_.
        permission_names (list[str]): The list of names of the permission to verify.

    Returns:
        Any: The role permission data.

    Raises:
        HTTPException: If the team_, permission, or role permission is not found.
    """

    log.info("team_id=%s, user_id=%s", team_id, user_id)
    team_member = get_team_member_by_team_user_id(team_id=team_id, user_id=user_id)
    if not team_member:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION
    role_permissions = await get_verified_role_permissions(role_id=team_member.role_id,
                                                           permission_names=permission_names)
    return role_permissions


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


async def add_new_team_member(user_id: UUID, team_id: UUID,
                              role_name: str) -> TeamMemberModel:
    """
    Add a new member to a team.

    Args:
        user_id (UUID): The ID of the new user.
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

    log.info("Checking if user already a member of the team.")
    member = get_team_member_by_team_user_id(team_id=team_id, user_id=user_id)
    if member:
        raise http_exceptions.ALREADY_MEMBER_EXCEPTION

    log.info("Create the team members.")
    team_member = {"user_id": user_id, "team_id": team_id, "role_id": role.id}
    return create_team_member(team_member)


async def get_single_team_response(team: TeamModel | None) -> SingleTeamResponse:
    """
    Generate the single team response from the TeamModel object with member count.
    TODO: We can further add assigned projects in Response

    Args:
        team (dict): SQLAlchemy model retrieved from db.

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
    await add_new_team_member(user_id=user_id, team_id=created_team.id, role_name=role_name)
    created_team = created_team.__dict__.copy()
    log.debug("Created team: %s", created_team)
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

    log.info("Updating the team response.")
    response_team = \
        {"items": sorted_teams, "total": total, "page": page, "size": size, "pages": pages}
    teams_with_count = []
    for team in sorted_teams:
        team_dict = team.__dict__.copy()
        team_dict["member_count"] = get_member_count_by_team_id(team.id)
        teams_with_count.append(team_dict)
        # teams_with_count.append(await get_single_team_response(team=team))

    response_team.update({"items": teams_with_count})
    return AllTeamResponse.model_validate(response_team)


async def get_team_by_team_id(team_id: UUID) -> SingleTeamResponse:
    """
    Retrieve the team by team ID.

    Args:
        team_id (UUID): The ID of the team.

    Raises:
        HTTPException: If team not found.

    Returns:
        SingleTeamResponse: The response for a specific ID.
    """
    log.info("Getting the team by team ID: %s", team_id)
    retrieved_team = get_team_by_id(team_id=team_id)
    if not retrieved_team:
        raise http_exceptions.TEAM_NOT_FOUND_EXCEPTION
    return await get_single_team_response(team=retrieved_team)


async def update_team_details(team_id: UUID, team_data: UpdateTeam) -> SingleTeamResponse:
    """
    Update the specific team details.

    Args:
        team_id (UUID): The ID of the team to be updated.
        team_data (UpdateTeam): The new details of the team.

    Raises:
        HTTPException: If team not found.

    Returns:
        SingleTeamResponse: The response for a specific ID.
    """
    log.info("Validate and converting the team_data")
    team_data = team_data.model_dump(exclude_unset=True)

    log.info("Updating team details for team: %s", team_id)
    updated_team = update_team(team_id=team_id, team_data=team_data)
    if not updated_team:
        raise http_exceptions.TEAM_NOT_FOUND_EXCEPTION

    log.debug("Updated data: %s", updated_team)
    return await get_single_team_response(team=updated_team)


async def delete_the_team_by_id(team_id: UUID) -> None:
    """
    Delete a specific team.

    Args:
        team_id (UUID): The ID of the team to be updated.

    Raises:
        HTTPException: If team not found
    """
    log.info('Deleting team: %s', team_id)
    deleted = delete_team(team_id=team_id)
    if not deleted:
        raise http_exceptions.TEAM_NOT_FOUND_EXCEPTION


async def add_team_members(org_id: UUID, team_id: UUID, user_roles: AddTeamMembersRequest
                           ) -> list[AddMemberResponse]:
    """
    Add a new member to the given team.

    Args:
        org_id (UUID): The ID of the organization of the team.
        team_id (UUID): The ID of the team.
        user_roles (AddTeamMembersRequest): The user roles has the user ID and the role name

    Raises:
         HTTPException: If user not found.

    Returns:
        list[AddMemberResponse]: List of the created user response.
    """
    members_response = []
    for user_role in user_roles.users:
        log.info("Getting the user details for user: %s", user_role.user_id)
        user = get_user_by_id(user_id=user_role.user_id)
        if not user:
            raise http_exceptions.USER_NOT_FOUND_EXCEPTION

        log.info("Adding member to the team.")
        added_member = await add_new_team_member(user_id=user_role.user_id,
                                               team_id=team_id, role_name=user_role.role_name)

        log.info("Generating the response for user: %s", user.id)
        team_member = {
            "id": user.id,  # changed from "user_id": user.id
            "email": user.email,
            "full_name": f"{user.first_name} {user.last_name}"
        }
        response = {
          "team_id": added_member.team_id,
          "organization_id": org_id,
          "role_id": added_member.role_id,
          "role_name": user_role.role_name,
          "user_details": team_member,
          "added_at": added_member.joined_at
        }
        members_response.append(AddMemberResponse.model_validate(response))

    return members_response
