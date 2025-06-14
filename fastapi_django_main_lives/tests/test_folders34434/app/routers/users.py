from fastapi import APIRouter, HTTPException
from app.schemas import UserSchema
from app.models import User
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.post("/users/")
async def create_user(username: str, password: str):
    user = User(username=username, password=password)
    session = sessionmaker(bind=engine)()
    session.add(user)
    session.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
async def read_users():
    session = sessionmaker(bind=engine)()
    users = session.query(User).all()
    return [UserSchema.from_orm(user) for user in users]