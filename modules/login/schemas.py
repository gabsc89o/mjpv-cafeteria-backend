from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema that represents a Token in the system
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema that represents data of Token
    """
    username: str | None = None