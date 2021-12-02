from typing import Optional
from pydantic import BaseModel
from pydantic.types import Optional


class TokenBase(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
