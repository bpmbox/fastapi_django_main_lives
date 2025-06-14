from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from app.crud.user import create_user, get_users, get_user, update_user
from app.schema.user import UserSchema
from app.main import get_db

router = APIRouter()

@router.post("/users/")
async def create_user_endpoint(user: UserSchema, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/users/")
async def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/users/{user_id}")
async def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@router.put("/users/{user_id}")
async def update_user_endpoint(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)