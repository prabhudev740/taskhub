import uuid
from sqlalchemy import Column, UUID, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
# from db.models.organization import OrganizationMemberModel
# from db.models.permission import PermissionModel
from db.base import Base


role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_system_role = Column(Boolean, default=False, nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True)

    organization_members = relationship("OrganizationMemberModel", back_populates="role")
    permissions = relationship("PermissionModel", secondary=role_permission, back_populates="roles")

