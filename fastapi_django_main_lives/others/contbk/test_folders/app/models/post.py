from dataclasses import dataclass
from app.models.user import User

@dataclass
class Post:
    id: int
    title: str
    content: str
    user: User

    def __init__(self, id: int, title: str, content: str, user: User):
        self.id = id
        self.title = title
        self.content = content
        self.user = user