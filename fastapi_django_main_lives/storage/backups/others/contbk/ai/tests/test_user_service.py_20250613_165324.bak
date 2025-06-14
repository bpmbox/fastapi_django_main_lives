import pytest
from src.services.user_service import UserService

def test_get_all_users():
    user_service = UserService()
    users = user_service.get_all_users()
    assert len(users) == 2
    assert users[0].name == "John Doe"
    assert users[1].name == "Jane Doe"