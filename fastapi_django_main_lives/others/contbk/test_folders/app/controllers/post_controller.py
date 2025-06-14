from app.models.post import Post
from app.models.user import User

class PostController:
    def __init__(self):
        self.posts = []

    def create_post(self, title: str, content: str, user: User) -> Post:
        post = Post(len(self.posts) + 1, title, content, user)
        self.posts.append(post)
        return post

    def get_posts(self) -> list[Post]:
        return self.posts