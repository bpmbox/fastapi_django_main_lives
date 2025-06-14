from pydantic import BaseModel
from app.models import Team

class TeamSchema(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True