""" Team Services. """

from  pprint import pprint
from uuid import UUID
from core.logging_conf import Logging
from db.crud.crud_team import get_team_by_name, create_team, get_member_count_by_team_id
from exceptions import http_exceptions
from schemas.team import CreateTeam, SingleTeamResponse


log = Logging(__name__).log()


async def add_new_team_in_organization(org_id: UUID, team: CreateTeam) -> SingleTeamResponse:
    """
    Create a new team for given organization_id.

    Args:
        org_id (UUID): The ID of the organization.
        team (CreateTeam): The team to be created.

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
    log.debug("Team to be created: %s", pprint(team_data))

    log.info("Creating new team '%s' in organization '%s'", team.name, org_id)
    created_team = create_team(team_data=team_data)
    member_count = get_member_count_by_team_id(team_id=created_team.id)
    created_team.member_count = member_count
    return SingleTeamResponse.model_validate(created_team)
