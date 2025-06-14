from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud

app = FastAPI()

@app.get("/users/")
async def read_users(db: Session = Depends()):
    users = crud.get_users(db)
    return {"users": users}

@app.post("/users/")
async def create_user(user: schemas.UserCreate, db: Session = Depends()):
    crud.create_user(db, user)
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends()):
    user = crud.get_user(db, user_id)
    return {"user": user}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends()):
    crud.update_user(db, user_id, user)
    return {"message": "User updated successfully"}

@app.post("/teams/")
async def create_team(team: schemas.TeamCreate, db: Session = Depends()):
    crud.create_team(db, team)
    return {"message": "Team created successfully"}

@app.get("/teams/")
async def read_teams(db: Session = Depends()):
    teams = crud.get_teams(db)
    return {"teams": teams}

@app.get("/teams/{team_id}")
async def read_team(team_id: int, db: Session = Depends()):
    team = crud.get_team(db, team_id)
    return {"team": team}