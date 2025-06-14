from sqlalchemy.orm import Session
from . import models, schema

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(username=user.username, password=user.password, profile=user.profile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()