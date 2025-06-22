import uuid
from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship
from db.base import Base
from db.models.role import role_permission


class PermissionModel(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String)

    roles = relationship("RoleModel", secondary=role_permission, back_populates="permissions")


