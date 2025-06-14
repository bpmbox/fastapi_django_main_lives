from src.models.transaction import Transaction
from src.repositories.transaction_repository import TransactionRepository

class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def create_transaction(self, account_id: int, amount: float, type: str) -> Transaction:
        # Create a new transaction for the account
        transaction = Transaction(id=1, account_id=account_id, amount=amount, type=type)  # Replace with actual ID generation
        self.transaction_repository.save(transaction)
        return transaction

    def get_transactions(self, account_id: int) -> list[Transaction]:
        return self.transaction_repository.get_all(account_id)