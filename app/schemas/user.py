from pydantic import BaseModel, Field
from uuid import UUID


class Notification(BaseModel):
    email_on_mention: bool
    push_on_task_assign: bool


class Preferences(BaseModel):
    language: str
    theme: str
    notifications: Notification | None


# class User(BaseModel):
#     id: UUID
#     email: str = Field(max_length=64)
#     full_name: str = Field(max_length=64)
#     is_active: bool
#     is_superuser: bool
#     created_at: str
#     updated_at: str
#     preferences: Preferences | None



class User(BaseModel):
    username: str
    email: str | None = None
    fullname: str | None = None
    disabled: bool | None = None
