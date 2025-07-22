""" Team Crud """

from uuid import UUID
from db.base import get_session
from db.models import OrganizationTeamModel
from db.models.team import TeamModel, TeamMemberModel


def create_team(team_data: dict[str, UUID]) -> TeamModel:
    """
    Create a new team in the database.

    Args:
        team_data (dict[str, UUID]): The team data to create a team.

    Returns:
        TeamModel: The newly created team.
    """
    team = TeamModel(**team_data)
    session = get_session()
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def create_team_member(team_member: dict[str, UUID]) -> TeamMemberModel:
    """
    Create a new team in the database.

    Args:
        team_member (dict[str, UUID]): The team data to create a team member.

    Returns:
        TeamMemberModel: The newly created team.
    """
    team_member = TeamMemberModel(**team_member)
    session = get_session()
    session.add(team_member)
    session.commit()
    session.refresh(team_member)
    return team_member


def get_team_by_id(team_id: UUID) -> TeamModel | None:
    """
    Retrieve the team by team ID from DB.

    Args:
        team_id (UUID): The ID of team to retrieve the team from db.

    Returns:
        TeamModel | None: The TeamModel instance if found, else None.
    """
    session = get_session()
    team = session.query(TeamModel).get(team_id)
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


def get_organization_teams(organization_id: UUID, page: int, size: int,
                              sort_by: str) -> tuple[list[type[TeamModel]], int, int]:
    """
    Retrieve the teams of the specific organization.

    Args:
        organization_id (str): ID of the organization.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        sort_by (str): Field to sort the organizations by.

    Returns:
         tuple[list[type[TeamModel]], int, int]: Retrieved data from TeamModel.
    """
    session = get_session()
    organization_teams = (session.query(TeamModel).join(OrganizationTeamModel,
                        TeamModel.organization_id == OrganizationTeamModel.organization_id)
                          .filter_by( organization_id=organization_id))

    sorted_teams = organization_teams.order_by(getattr(TeamModel, sort_by))
    total = sorted_teams.count()
    sorted_teams = sorted_teams.offset((page - 1) * size).limit(size).all()
    pages = (total + size - 1) // size
    return sorted_teams, total, pages


def update_team(team_id: UUID, team_data: dict) -> TeamModel | None:
    """
    Update the team in database.

    Args:
        team_id (UUID): The ID of the team to be updated.
        team_data (UpdateTeam): The new details of the team.

    Returns:
        TeamModel | None: TeamModel if updated successful, else None.
    """
    session = get_session()
    team = session.query(TeamModel).get(team_id)
    if not team:
        return None
    for key, val in team_data.items():
        setattr(team, key, val)
    session.commit()
    session.refresh(team)
    return team


def delete_team(team_id: UUID) -> bool:
    """
    Delete a team from the database.

    Args:
        team_id (UUID): The ID of the team to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    session = get_session()
    team = session.query(TeamModel).get(team_id)
    if not team:
        return False
    session.delete(team)
    session.commit()
    return True

def get_team_member_by_team_user_id(team_id: UUID, user_id: UUID) -> type[TeamMemberModel] | None:
    """
    Retrieve a team member by team ID and user ID.

    Args:
        team_id (UUID): The ID of the team.
        user_id (UUID): The ID of the user.

    Returns:
        type[TeamMemberModel] | None: The organization member if found, otherwise None.
    """
    session = get_session()
    team_member = \
        session.query(TeamMemberModel).filter_by(user_id=user_id, team_id=team_id).first()
    if not team_member:
        return None
    return team_member
