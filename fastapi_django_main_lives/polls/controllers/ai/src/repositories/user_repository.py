from src.models.user import User

class UserRepository:
    def __init__(self):
        self.users = {}  # Replace with actual database connection

    def save(self, user: User):
        self.users[user.id] = user

    def get(self, id: int) -> User:
        return self.users.get(id)