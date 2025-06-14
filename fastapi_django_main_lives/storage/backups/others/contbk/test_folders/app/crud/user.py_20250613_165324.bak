from app.models.user import User
from app.schema.user import UserSchema
from sqlalchemy.orm import Session

def create_user(db: Session, user: UserSchema):
    db_user = User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserSchema):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.username = user.username
        db_user.password = user.password
        db_user.profile = user.profile
        db_user.team_id = user.team_id
        db.commit()
        db.refresh(db_user)
    return db_user