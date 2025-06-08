from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    profile: str
    tags: List[str]