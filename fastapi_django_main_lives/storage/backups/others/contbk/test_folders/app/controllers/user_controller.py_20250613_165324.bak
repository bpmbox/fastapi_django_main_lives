from app.models.user import User

class UserController:
    def __init__(self):
        self.users = []

    def create_user(self, name: str, email: str) -> User:
        user = User(len(self.users) + 1, name, email)
        self.users.append(user)
        return user

    def get_users(self) -> list[User]:
        return self.users