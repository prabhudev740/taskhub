""" User Model """

import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, String, Column, UUID, DateTime, func
from db.base import Base

# pylint: disable=too-few-public-methods
# pylint: disable=not-callable


class UserModel(Base):
    """
    Represents a user entity in the database.

    Attributes:
        id (UUID): Unique identifier for the user (primary key).
        first_name (str): First name of the user (not nullable).
        last_name (str): Last name of the user (not nullable).
        username (str): Unique username of the user (not nullable, indexed).
        email (str): Unique email address of the user (not nullable).
        hashed_password (str): Hashed password of the user (not nullable).
        is_active (bool): Indicates if the user is active (default is True, indexed).
        is_superuser (bool): Indicates if the user has superuser privileges
        (default is False, indexed).
        created_at (DateTime): Timestamp when the user was created (default is current time).
        updated_at (DateTime): Timestamp when the user was last updated
        (default is current time).
        last_login_at (DateTime): Timestamp of the user's last login (nullable).
        memberships (relationship): Relationship to organization memberships
        associated with the user.
    """
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
        """
        Returns the string representation of the UserModel class.

        Returns:
            str: The table name associated with the UserModel class.
        """
        return UserModel.__tablename__
