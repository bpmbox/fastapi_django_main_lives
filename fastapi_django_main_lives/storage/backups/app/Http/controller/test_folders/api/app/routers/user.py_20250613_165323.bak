from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserSchema

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserSchema, session: Session = Depends()):
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, profile=user.profile, tags=user.tags)
    session.add(new_user)
    session.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
async def get_users(session: Session = Depends()):
    users = session.query(User).all()
    return [{"username": user.username, "profile": user.profile} for user in users]