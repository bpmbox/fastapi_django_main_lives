from src.models.account import Account
from src.repositories.account_repository import AccountRepository

class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def create_account(self, user_id: int) -> Account:
        # Create a new account for the user
        account = Account(id=1, user_id=user_id)  # Replace with actual ID generation
        self.account_repository.save(account)
        return account

    def get_account(self, id: int) -> Account:
        return self.account_repository.get(id)