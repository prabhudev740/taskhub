""" Models for Teams """

import uuid
from sqlalchemy import Column, UUID, String, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.base import Base

# pylint: disable=too-few-public-methods
# pylint: disable=not-callable


class TeamModel(Base):
    """
    Represents the team entity in database.

    Attributes:
        id (UUID): The ID of the team.
        name (str): The name of the team.
        description (str): The description of team.
        created_at (DateTime): Timestamp when the team was created.
        updated_at (DateTime): Timestamp when the organization was created.
        members (relationship): Relationship to the team members.
        organization_teams (relationship): Relationship to the organization teams.
        organizations (relationship): Relationship to the organizations.
    """
    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint("organization_id", "name", name="uq_team_org_name"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), index=True, nullable=False)
    description = Column(String, nullable=True)
    organization_id = Column(UUID(as_uuid=True),
                             ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                        server_onupdate=func.now())

    members = relationship("TeamMemberModel", back_populates="team",
                           cascade="all, delete-orphan")
    organization_teams = relationship("OrganizationTeamModel", back_populates="team",
                                      overlaps="teams")
    organizations = relationship("OrganizationModel", secondary="organization_teams",
                                 back_populates="teams",
                                 overlaps="organization_teams,team,organization")


class TeamMemberModel(Base):
    """
    Represents team members entity in database.

    Attributes:
        team_id (UUID): The ID of the team.
        user_id (UUID): The ID of the member of the team.
        joined_at (DateTime): Timestamp when user joined the team.
        team (relationship): Relationship to the teams.
        user (relationship): Relationship to the users.
    """
    __tablename__ = "team_members"

    team_id = Column(UUID(as_uuid=True),
                     ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True),
                     ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    team = relationship("TeamModel", back_populates="members")
    user = relationship("UserModel", back_populates="team_memberships")
