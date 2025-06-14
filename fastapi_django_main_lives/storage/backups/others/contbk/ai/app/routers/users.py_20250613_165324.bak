from fastapi import APIRouter, HTTPException
from app.schemas import UserSchema
from app.models import User

router = APIRouter()

@router.post("/register")
async def register_user(user: UserSchema):
    # Check if username already exists
    existing_user = User.query.filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id, tags=user.tags)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}

@router.get("/users")
async def get_users():
    users = User.query.all()
    return [{"id": user.id, "username": user.username, "profile": user.profile} for user in users]

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = User.query.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "profile": user.profile, "tags": user.tags}