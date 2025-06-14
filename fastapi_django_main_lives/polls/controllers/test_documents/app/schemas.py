from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    profile: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass