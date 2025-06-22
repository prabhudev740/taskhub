import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, String, Column, UUID, DateTime, func
from db.base import Base
from db.models.organization import OrganizationMemberModel


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(64), unique=True, nullable=False)
    hashed_password = Column(String(64), nullable=False)

    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    # updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    # Relationship to members
    memberships = relationship("OrganizationMemberModel", back_populates="users")

    def __repr__(self):
        return UserModel.__tablename__



