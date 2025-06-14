from fastapi import APIRouter
from . import crud
from . import schema

router = APIRouter()

@router.post("/users/")
def create_user(user: schema.UserCreate):
    return crud.create_user(user=user)

@router.get("/users/")
def read_users(skip: int = 0, limit: int = 100):
    return crud.get_users(skip=skip, limit=limit)

@router.get("/users/{user_id}")
def read_user(user_id: int):
    return crud.get_user(user_id=user_id)