from app.routes import *

def main():
    user1 = create_user("John Doe", "john@example.com")
    user2 = create_user("Jane Doe", "jane@example.com")

    post1 = create_post("Hello World", "This is my first post", user1)
    post2 = create_post("Hello Again", "This is my second post", user2)

    comment1 = create_comment("Nice post!", post1, user1)
    comment2 = create_comment("Great post!", post2, user2)

    print("Users:", get_users())
    print("Posts:", get_posts())
    print("Comments:", get_comments())

if __name__ == "__main__":
    main()