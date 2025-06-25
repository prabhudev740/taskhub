""" User Schemas """

from uuid import UUID
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class Notification(BaseModel):
    email_on_mention: bool
    push_on_task_assign: bool


class Preferences(BaseModel):
    language: str
    theme: str
    notifications: Notification | None


class UserProfile(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileShort(BaseModel):
    id: UUID
    full_name: str
    email: str


class User(UserProfile):
    is_active: bool
    updated_at: datetime
    last_login_at: datetime | None = None


class CreateUser(BaseModel):
    first_name: Annotated[str, Field(min_length=2)]
    last_name: Annotated[str, Field(min_length=2)]
    username: Annotated[str, Field(min_length=5)]
    email: Annotated[str, Field(min_length=5)]
    password: Annotated[str, Field(min_length=8)]


class UpdateUser(BaseModel):
    first_name: Annotated[str | None, Field(min_length=2, default=None)]
    last_name: Annotated[str | None, Field(min_length=2, default=None)]
    email: Annotated[str | None, Field(min_length=5, default=None)]
    is_active: Annotated[bool | None, Field(default=None)]


class UserPasswordUpdate(BaseModel):
    password: Annotated[str, Field(min_length=8)]
    new_password: Annotated[str, Field(min_length=8)]
    confirm_new_password: Annotated[str, Field(min_length=8)]


class UserMessageResponse(BaseModel):
    message: str
