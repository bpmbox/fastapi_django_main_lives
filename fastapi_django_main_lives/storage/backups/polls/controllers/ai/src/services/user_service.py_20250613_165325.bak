from src.models.user import User
from src.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, name: str, email: str) -> User:
        # Create a new user
        user = User(id=1, name=name, email=email)  # Replace with actual ID generation
        self.user_repository.save(user)
        return user

    def get_user(self, id: int) -> User:
        return self.user_repository.get(id)