from api.models import User
from api.schemas import UserSchema

def get_user(user_id: int):
    return session.query(User).get(user_id)

def update_user(user_id: int, profile: str, tags: List[str]):
    user = session.query(User).get(user_id)
    user.profile = profile
    user.tags = tags
    session.commit()
    return user