""" Permission Model """
import uuid
from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship
from db.base import Base

# pylint: disable=too-few-public-methods


class PermissionModel(Base):
    """
    Represents a permission entity in the database.

    Attributes:
        id (UUID): Unique identifier for the permission (primary key).
        name (str): Name of the permission (must be unique and not nullable).
        description (str): Optional description of the permission.
        roles (relationship): Relationship to roles associated with the permission.
    """
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String)

    roles = relationship("RoleModel", secondary="role_permission", back_populates="permissions")
