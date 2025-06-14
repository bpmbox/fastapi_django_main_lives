from fastapi import APIRouter, HTTPException
from app.schemas import UserSchema
from app.models import User
from sqlalchemy.orm import sessionmaker

router = APIRouter()

@router.post("/register")
async def register_user(user: UserSchema):
    # Check if user already exists
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id, tags=user.tags)
    session.add(new_user)
    session.commit()
    return {"message": "User created successfully"}

@router.get("/users")
async def get_users():
    users = session.query(User).all()
    return [{"username": user.username, "profile": user.profile, "team_id": user.team_id, "tags": user.tags} for user in users]

@router.get("/users/{username}")
async def get_user(username: str):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "profile": user.profile, "team_id": user.team_id, "tags": user.tags}