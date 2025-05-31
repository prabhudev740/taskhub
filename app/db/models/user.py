from datetime import datetime
from schemas.user import User
from sqlalchemy import Boolean, String, Column, UUID, DateTime, ForeignKey
from db.base import Base

class UserInDB(User):
    hashed_password: str


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(64), unique=True, nullable=False, index=True)
    hashed_password = Column(String(64), nullable=False)

    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    organizations_id = Column(UUID, ForeignKey("organization.id"), primary_key=True)




