from src.models.account import Account
from src.repositories.account_repository import AccountRepository
from src.services.account_service import AccountService

def test_create_account():
    account_repository = AccountRepository()
    account_service = AccountService(account_repository)
    account = account_service.create_account(1)
    assert isinstance(account, Account)