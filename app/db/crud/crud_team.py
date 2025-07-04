""" Team Crud """

from uuid import UUID
from db.base import get_session
from db.models.team import TeamModel, TeamMemberModel


def create_team(team_data: dict) -> TeamModel:
    """
    Create a new team in the database.

    Args:
        team_data (dict): The team data to create a team.

    Returns:
        TeamModel: The newly created team.
    """
    team = TeamModel(**team_data)
    session = get_session()
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def get_team_by_id(team_id: UUID) -> type[TeamModel] | None:
    """
    Retrieve the team by team ID from DB.

    Args:
        team_id (UUID): The ID of team to retrieve the team from db.

    Returns:
        type[TeamModel] | None: type[TeamModel] if team found else None.
    """
    session = get_session()
    team = session.query(TeamModel).filter_by(id=team_id).first()
    if not team:
        return None
    return team


def get_team_by_name(team_name: str, org_id: UUID) -> type[TeamModel] | None:
    """
    Retrieve the team by team name from DB.

    Args:
        team_name (str): The name of team to retrieve the team from db.
        org_id (UUID): The ID of the organization to create a team.

    Returns:
        type[TeamModel] | None: type[TeamModel] if team found else None.
    """
    session = get_session()
    team = session.query(TeamModel).filter_by(name=team_name, organization_id=org_id).first()
    if not team:
        return None
    return team


def get_member_count_by_team_id(team_id: UUID) -> int:
    """
    Retrieve the count of members from database.

    Args:
        team_id (UUID): The ID of team to retrieve.

    Returns:
        int: Count of the members of the team.
    """
    session = get_session()
    member_count = session.query(TeamMemberModel).filter_by(team_id=team_id).count()
    return member_count
