from app.controllers.user_controller import UserController
import pytest

def test_create_user():
    user_controller = UserController()
    user = user_controller.create_user("John Doe", "john@example.com")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_get_users():
    user_controller = UserController()
    user1 = user_controller.create_user("John Doe", "john@example.com")
    user2 = user_controller.create_user("Jane Doe", "jane@example.com")
    users = user_controller.get_users()
    assert len(users) == 2
    assert users[0].name == "John Doe"
    assert users[1].name == "Jane Doe"