from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
from uuid import UUID


class Notification(BaseModel):
    email_on_mention: bool
    push_on_task_assign: bool


class Preferences(BaseModel):
    language: str
    theme: str
    notifications: Notification | None


class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}


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


class UserProfile(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserMessageResponse(BaseModel):
    message: str
