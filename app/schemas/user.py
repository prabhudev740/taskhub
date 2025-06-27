""" User Schemas """

from uuid import UUID
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class Notification(BaseModel):
    """
    Represents notification preferences for a user.

    Attributes:
        email_on_mention (bool): Indicates if the user wants email notifications on mentions.
        push_on_task_assign (bool): Indicates if the user wants push notifications on
        task assignments.
    """
    email_on_mention: bool
    push_on_task_assign: bool


class Preferences(BaseModel):
    """
    Represents user preferences.

    Attributes:
        language (str): Preferred language of the user.
        theme (str): Preferred theme of the user.
        notifications (Notification | None): Notification preferences (optional).
    """
    language: str
    theme: str
    notifications: Notification | None


class UserProfile(BaseModel):
    """
    Represents a detailed user profile.

    Attributes:
        id (UUID): Unique identifier for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        is_active (bool): Indicates if the user is active.
        created_at (datetime): Timestamp when the user was created.
    """
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileShort(BaseModel):
    """
    Represents a shortened user profile.

    Attributes:
        id (UUID): Unique identifier for the user.
        full_name (str): Full name of the user.
        email (str): Email address of the user.
    """
    id: UUID
    full_name: str
    email: str


class User(UserProfile):
    """
    Represents a user with additional attributes.

    Attributes:
        is_active (bool): Indicates if the user is active.
        updated_at (datetime): Timestamp when the user was last updated.
        last_login_at (datetime | None): Timestamp of the user's last login (optional).
    """
    is_active: bool
    updated_at: datetime
    last_login_at: datetime | None = None


class CreateUser(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        first_name (Annotated[str, Field]): First name of the user (minimum length: 2).
        last_name (Annotated[str, Field]): Last name of the user (minimum length: 2).
        username (Annotated[str, Field]): Username of the user (minimum length: 5).
        email (Annotated[str, Field]): Email address of the user (minimum length: 5).
        password (Annotated[str, Field]): Password for the user (minimum length: 8).
    """
    first_name: Annotated[str, Field(min_length=2)]
    last_name: Annotated[str, Field(min_length=2)]
    username: Annotated[str, Field(min_length=5)]
    email: Annotated[str, Field(min_length=5)]
    password: Annotated[str, Field(min_length=8)]


class UpdateUser(BaseModel):
    """
    Schema for updating user details.

    Attributes:
        first_name (Annotated[str | None, Field]): Updated first name of the user
        (optional, minimum length: 2).
        last_name (Annotated[str | None, Field]): Updated last name of the user
        (optional, minimum length: 2).
        email (Annotated[str | None, Field]): Updated email address of the user
         (optional, minimum length: 5).
        is_active (Annotated[bool | None, Field]): Updated active status of the user (optional).
    """
    first_name: Annotated[str | None, Field(min_length=2, default=None)]
    last_name: Annotated[str | None, Field(min_length=2, default=None)]
    email: Annotated[str | None, Field(min_length=5, default=None)]
    is_active: Annotated[bool | None, Field(default=None)]


class UserPasswordUpdate(BaseModel):
    """
    Schema for updating a user's password.

    Attributes:
        password (Annotated[str, Field]): Current password of the user (minimum length: 8).
        new_password (Annotated[str, Field]): New password for the user (minimum length: 8).
        confirm_new_password (Annotated[str, Field]): Confirmation of the new password
        (minimum length: 8).
    """
    password: Annotated[str, Field(min_length=8)]
    new_password: Annotated[str, Field(min_length=8)]
    confirm_new_password: Annotated[str, Field(min_length=8)]


class UserMessageResponse(BaseModel):
    """
    Response schema for user-related messages.

    Attributes:
        message (str): Message content.
    """
    message: str
