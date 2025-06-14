from app.controllers.post_controller import PostController
from app.models.user import User
import pytest

def test_create_post():
    post_controller = PostController()
    user = User(1, "John Doe", "john@example.com")
    post = post_controller.create_post("Hello World", "This is my first post", user)
    assert post.title == "Hello World"
    assert post.content == "This is my first post"
    assert post.user == user

def test_get_posts():
    post_controller = PostController()
    user = User(1, "John Doe", "john@example.com")
    post1 = post_controller.create_post("Hello World", "This is my first post", user)
    post2 = post_controller.create_post("Hello Again", "This is my second post", user)
    posts = post_controller.get_posts()
    assert len(posts) == 2
    assert posts[0].title == "Hello World"
    assert posts[1].title == "Hello Again"