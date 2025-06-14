from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str
    profile: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True