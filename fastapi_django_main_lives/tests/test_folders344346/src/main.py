from src.services.user_service import UserService

def main():
    user_service = UserService()
    users = user_service.get_all_users()
    for user in users:
        print(user)

if __name__ == "__main__":
    main()