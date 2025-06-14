from pydantic import BaseModel
from typing import List

class UserSchema(BaseModel):
    id: int
    username: str
    profile: str
    tags: List[str]
    team: str