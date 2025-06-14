from dataclasses import dataclass
from app.models.post import Post
from app.models.user import User

@dataclass
class Comment:
    id: int
    content: str
    post: Post
    user: User

    def __init__(self, id: int, content: str, post: Post, user: User):
        self.id = id
        self.content = content
        self.post = post
        self.user = user