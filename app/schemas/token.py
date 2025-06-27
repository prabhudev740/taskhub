""" Token """
from typing import Any
from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents an authentication token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., "Bearer").
        expires_in (int | None): The expiration time of the token in seconds (optional).
        refresh_token (str | None): The refresh token string (optional).
        scope (str | None): The scope of the token (optional).
        user_info (dict[str, Any] | None): Additional user information associated with the
        token (optional).
    """
    access_token: str
    token_type: str
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: str | None = None
    user_info: dict[str, Any] | None = None


class TokenData(BaseModel):
    """
    Represents the data associated with a token.

    Attributes:
        username (str): The username associated with the token.
    """
    username: str
