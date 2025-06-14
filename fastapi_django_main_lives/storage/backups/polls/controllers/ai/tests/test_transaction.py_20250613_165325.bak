from src.models.transaction import Transaction
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_service import TransactionService

def test_create_transaction():
    transaction_repository = TransactionRepository()
    transaction_service = TransactionService(transaction_repository)
    transaction = transaction_service.create_transaction(1, 100.0, "deposit")
    assert isinstance(transaction, Transaction)