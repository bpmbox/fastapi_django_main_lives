from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

def test_create_user():
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    user = user_service.create_user("John Doe", "john@example.com")
    assert isinstance(user, User)