from src.services.account_service import AccountService
from src.services.transaction_service import TransactionService
from src.services.user_service import UserService

def main():
    account_repository = AccountRepository()
    transaction_repository = TransactionRepository()
    user_repository = UserRepository()

    account_service = AccountService(account_repository)
    transaction_service = TransactionService(transaction_repository)
    user_service = UserService(user_repository)

    user = user_service.create_user("John Doe", "john@example.com")
    account = account_service.create_account(user.id)

    transaction_service.create_transaction(account.id, 100.0, "deposit")

if __name__ == "__main__":
    main()