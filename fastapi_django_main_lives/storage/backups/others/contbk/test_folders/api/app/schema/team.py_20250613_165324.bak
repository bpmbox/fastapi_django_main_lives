from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True