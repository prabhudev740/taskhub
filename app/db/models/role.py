""" Role Model """
import uuid
from sqlalchemy import Column, UUID, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base

# pylint: disable=too-few-public-methods


class RolePermissionModel(Base):
    """
    Represents the association between roles and permissions in the database.

    Attributes:
        role_id (UUID): The unique identifier of the role (primary key).
        permission_id (UUID): The unique identifier of the permission (primary key).
    """
    __tablename__ = "role_permission"

    role_id = Column(UUID(as_uuid=True),
                     ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(UUID(as_uuid=True),
                           ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)


class RoleModel(Base):
    """
    Represents a role entity in the database.

    Attributes:
        id (UUID): Unique identifier for the role (primary key).
        name (str): Name of the role (must be unique).
        description (str): Optional description of the role.
        is_system_role (bool): Indicates if the role is a system role.
        organization_id (UUID): ID of the associated organization (optional).
        organization_members (relationship): Relationship to organization members.
        permissions (relationship): Relationship to permissions associated with the role.
    """
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_system_role = Column(Boolean, default=False, nullable=False)
    organization_id = Column(UUID, ForeignKey("organizations.id"), nullable=True)

    organization_members = relationship("OrganizationMemberModel", back_populates="role")
    permissions = relationship("PermissionModel",
                               secondary="role_permission", back_populates="roles")
