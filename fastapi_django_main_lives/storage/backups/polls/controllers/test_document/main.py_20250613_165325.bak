from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import User, Team
from database import engine, SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
async def register_user(username: str, password: str, db: Session = Depends(get_db)):
    if User.exists(username, db):
        return {"error": "Username already exists"}
    user = User(username, password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login")
async def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = User.authenticate(username, password, db)
    if user:
        return {"message": "Login successful"}
    return {"error": "Invalid username or password"}

@app.get("/teams")
async def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).order_by(Team.created_at.desc()).all()
    return [{"id": team.id, "name": team.name} for team in teams]

@app.post("/teams")
async def create_team(name: str, db: Session = Depends(get_db)):
    team = Team(name)
    db.add(team)
    db.commit()
    return {"message": "Team created successfully"}

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{"id": user.id, "username": user.username, "profile": user.profile} for user in users]

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return {"username": user.username, "team": user.team.name, "profile": user.profile, "tags": user.tags}
    return {"error": "User not found"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, team_id: int, profile: str, tags: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.team_id = team_id
        user.profile = profile
        user.tags = tags
        db.commit()
        return {"message": "User updated successfully"}
    return {"error": "User not found"}