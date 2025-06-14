from src.models.transaction import Transaction

class TransactionRepository:
    def __init__(self):
        self.transactions = {}  # Replace with actual database connection

    def save(self, transaction: Transaction):
        self.transactions[transaction.id] = transaction

    def get_all(self, account_id: int) -> list[Transaction]:
        return [t for t in self.transactions.values() if t.account_id == account_id]