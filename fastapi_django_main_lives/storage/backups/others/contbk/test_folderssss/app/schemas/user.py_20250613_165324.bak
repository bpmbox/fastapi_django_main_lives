from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str
    profile: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    team_id: int
    team_name: str