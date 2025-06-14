from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database import engine, SessionLocal
from models.user import User
from schemas.user import UserCreate, UserRead

router = APIRouter()

@router.get("/api/users")
async def read_users(db: SessionLocal = Depends()):
    users = db.query(User).all()
    return JSONResponse(status_code=200, content=[UserRead.from_orm(user) for user in users])

@router.get("/api/users/{user_id}")
async def read_user(user_id: int, db: SessionLocal = Depends()):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return JSONResponse(status_code=200, content=UserRead.from_orm(user))

@router.put("/api/users/{user_id}")
async def update_user(user_id: int, user: UserCreate, db: SessionLocal = Depends()):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    db_user.username = user.username
    db_user.password = user.password
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User updated successfully"})