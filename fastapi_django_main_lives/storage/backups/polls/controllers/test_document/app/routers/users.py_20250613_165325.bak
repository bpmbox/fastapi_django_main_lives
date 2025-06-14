from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.utils import get_authorization_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserSchema
from app.main import async_session

router = APIRouter()

@router.post("/register")
async def register_user(username: str, password: str, db: AsyncSession = Depends()):
    if await db.execute(User.__table__.select().where(User.username == username)).scalar():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password=password)
    db.add(user)
    await db.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
async def read_users(db: AsyncSession = Depends()):
    users = await db.execute(User.__table__.select())
    return [{"username": user.username, "profile": user.profile} for user in users]

@router.get("/users/{username}")
async def read_user(username: str, db: AsyncSession = Depends()):
    user = await db.execute(User.__table__.select().where(User.username == username))
    if user:
        return {"username": user.username, "profile": user.profile}
    raise HTTPException(status_code=404, detail="User not found")