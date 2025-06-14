from pydantic import BaseModel

class TeamCreate(BaseModel):
    name: str

class TeamRead(BaseModel):
    id: int
    name: str
    created_at: datetime