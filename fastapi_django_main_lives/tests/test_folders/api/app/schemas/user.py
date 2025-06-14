from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    profile: str
    team_id: int