from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, User
from app.models import User as UserModel

router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends()):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = UserModel(username=user.username, password=user.password, profile=user.profile)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
def read_users(db: Session = Depends()):
    users = db.query(UserModel).all()
    return [{"id": user.id, "username": user.username, "profile": user.profile} for user in users]