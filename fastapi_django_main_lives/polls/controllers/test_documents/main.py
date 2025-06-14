from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import User, Team
from schemas import UserCreate, UserUpdate, TeamCreate
from database import get_db

app = FastAPI()

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends()):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/teams/")
def create_team(team: TeamCreate, db: Session = Depends()):
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    return {"message": "Team created successfully"}

@app.get("/users/")
def read_users(db: Session = Depends()):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username} for user in users]

@app.get("/teams/")
def read_teams(db: Session = Depends()):
    teams = db.query(Team).all()
    return [{"id": team.id, "name": team.name} for team in teams]

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends()):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return {"error": "User not found"}
    return {"id": user.id, "username": user.username, "profile": user.profile, "tags": user.tags}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends()):
    user_db = db.query(User).filter(User.id == user_id).first()
    if user_db is None:
        return {"error": "User not found"}
    user_db.username = user.username
    user_db.profile = user.profile
    user_db.tags = user.tags
    db.commit()
    return {"message": "User updated successfully"}