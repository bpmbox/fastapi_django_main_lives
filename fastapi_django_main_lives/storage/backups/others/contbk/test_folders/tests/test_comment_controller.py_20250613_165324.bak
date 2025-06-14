from app.controllers.comment_controller import CommentController
from app.models.post import Post
from app.models.user import User
import pytest

def test_create_comment():
    comment_controller = CommentController()
    user = User(1, "John Doe", "john@example.com")
    post = Post(1, "Hello World", "This is my first post", user)
    comment = comment_controller.create_comment("Nice post!", post, user)
    assert comment.content == "Nice post!"
    assert comment.post == post
    assert comment.user == user

def test_get_comments():
    comment_controller = CommentController()
    user = User(1, "John Doe", "john@example.com")
    post = Post(1, "Hello World", "This is my first post", user)
    comment1 = comment_controller.create_comment("Nice post!", post, user)
    comment2 = comment_controller.create_comment("Great post!", post, user)
    comments = comment_controller.get_comments()
    assert len(comments) == 2
    assert comments[0].content == "Nice post!"
    assert comments[1].content == "Great post!"