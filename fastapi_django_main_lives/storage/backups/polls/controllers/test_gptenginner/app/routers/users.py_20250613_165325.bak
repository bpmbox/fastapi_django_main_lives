from fastapi import APIRouter, HTTPException
from app.schemas import UserSchema
from app.models import User
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.post("/register")
async def register_user(username: str, password: str):
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
async def read_users():
    users = session.query(User).all()
    return [{"id": user.id, "username": user.username, "profile": user.profile} for user in users]

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "profile": user.profile}