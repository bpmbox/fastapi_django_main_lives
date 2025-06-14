from src.repositories.user_repository import UserRepository

class UserService:
    """Handles user business logic"""
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, name, email):
        """Creates a new user"""
        return self.user_repository.create_user(name, email)