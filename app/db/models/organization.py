import uuid

from sqlalchemy import Column, UUID, String, Text, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from db.models.role import RoleModel


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to members
    members = relationship("OrganizationMemberModel", back_populates="organization")
    # owner = relationship("User") # If you have owner_id


class OrganizationMemberModel(Base):
    __tablename__ = "organization_members"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
                             primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    users = relationship("UserModel", back_populates="memberships")
    organization = relationship("OrganizationModel", back_populates="members")
    role = relationship("RoleModel", back_populates="organization_members")


# if __name__ == "__main__":
#     create_db_and_tables()
#     session = get_session()
#     new_org = Organization(name="Prabhu1")
#     session.add(new_org)
#     session.commit()