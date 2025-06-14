from app.controllers.user_controller import UserController
from app.controllers.post_controller import PostController
from app.controllers.comment_controller import CommentController

user_controller = UserController()
post_controller = PostController()
comment_controller = CommentController()

def get_users():
    return user_controller.get_users()

def create_user(name: str, email: str):
    return user_controller.create_user(name, email)

def get_posts():
    return post_controller.get_posts()

def create_post(title: str, content: str, user: User):
    return post_controller.create_post(title, content, user)

def get_comments():
    return comment_controller.get_comments()

def create_comment(content: str, post: Post, user: User):
    return comment_controller.create_comment(content, post, user)