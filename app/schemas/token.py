from pydantic import BaseModel
from typing import Any


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: str | None = None
    user_info: dict[str, Any] | None = None

class TokenData(BaseModel):
    username: str
