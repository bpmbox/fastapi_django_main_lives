from pydantic import BaseModel

class TeamSchema(BaseModel):
    id: int
    name: str