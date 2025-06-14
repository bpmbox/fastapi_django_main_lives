from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserSchema

router = APIRouter()

@router.post("/register")
async def register_user(user: UserSchema, db: Session = Depends()):
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.get("/users")
async def get_users(db: Session = Depends()):
    users = db.query(User).all()
    return [{"username": user.username, "profile": user.profile} for user in users]