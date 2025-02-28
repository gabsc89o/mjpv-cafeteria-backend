"""
Team: MSG - AXIANS

Module that contains schemas for database models.
"""
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocalUser(BaseModel):
    """
    Schema that represents an local user in the database.
    """
    id: int | None = None
    username: str
    password_hash: Optional[str] = None

    model_config = ConfigDict(
        from_attributes = True
    )
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            username=obj.username,
            password_hash=obj.password_hash,
        )
        

class RequestLocalUser(BaseModel):
    """
    Schema that represents an local user request in the API.
    """
    username: str
    password: str
