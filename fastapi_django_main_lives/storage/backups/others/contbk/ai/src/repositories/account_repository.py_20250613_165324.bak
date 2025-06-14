from src.models.account import Account

class AccountRepository:
    def __init__(self):
        self.accounts = {}  # Replace with actual database connection

    def save(self, account: Account):
        self.accounts[account.id] = account

    def get(self, id: int) -> Account:
        return self.accounts.get(id)