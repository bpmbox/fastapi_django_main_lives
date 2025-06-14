from src.models.user import User

class UserRepository:
    """Handles user data access"""
    def __init__(self):
        self.users = []

    def create_user(self, name, email):
        """Creates a new user"""
        user = User(name, email)
        self.users.append(user)
        return user