from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User

class CommentController:
    def __init__(self):
        self.comments = []

    def create_comment(self, content: str, post: Post, user: User) -> Comment:
        comment = Comment(len(self.comments) + 1, content, post, user)
        self.comments.append(comment)
        return comment

    def get_comments(self) -> list[Comment]:
        return self.comments