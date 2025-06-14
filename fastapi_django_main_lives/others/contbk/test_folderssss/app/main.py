from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers import user, team

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic app!"}

app.include_router(user.router)
app.include_router(team.router)