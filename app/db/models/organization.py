""" ORG Model """
import uuid

from sqlalchemy import Column, UUID, String, Text, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

# pylint: disable=too-few-public-methods
# pylint: disable=not-callable


class OrganizationModel(Base):
    """
    Represents an organization entity in the database.

    Attributes:
        id (UUID): Unique identifier for the organization.
        name (str): Name of the organization (must be unique).
        description (str): Optional description of the organization.
        owner_id (UUID): ID of the user who owns the organization.
        created_at (datetime): Timestamp when the organization was created.
        updated_at (datetime): Timestamp when the organization was last updated.
        members (relationship): Relationship to the organization members.
    """
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # pylint: disable=not-callable
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)  # pylint: disable=not-callable

    # Relationship to members
    members = relationship("OrganizationMemberModel", back_populates="organization")
    # owner = relationship("User") # If you have owner_id


class OrganizationMemberModel(Base):
    """
    Represents a member of an organization in the database.

    Attributes:
        user_id (UUID): Unique identifier for the user (primary key).
        organization_id (UUID): Unique identifier for the organization (primary key).
        role_id (UUID): ID of the role assigned to the user in the organization.
        joined_at (datetime): Timestamp when the user joined the organization.
        users (relationship): Relationship to the user entity.
        organization (relationship): Relationship to the organization entity.
        role (relationship): Relationship to the role entity.
    """
    __tablename__ = "organization_members"

    user_id = Column(UUID(as_uuid=True),
                     ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key=True)
    organization_id = Column(UUID(as_uuid=True),
                             ForeignKey("organizations.id", ondelete="CASCADE"),
                             primary_key=True)
    role_id = Column(UUID(as_uuid=True),
                     ForeignKey("roles.id", ondelete="CASCADE"),
                     nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # pylint: disable=not-callable

    users = relationship("UserModel", back_populates="memberships")
    organization = relationship("OrganizationModel", back_populates="members")
    role = relationship("RoleModel", back_populates="organization_members")
