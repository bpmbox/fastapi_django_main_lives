from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from api.models import Base
from api.schemas import UserSchema, TeamSchema
from api.crud import user, team

app = FastAPI()

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.post("/register")
async def register_user(username: str, password: str):
    # Register user logic
    pass

@app.post("/login")
async def login_user(username: str, password: str):
    # Login user logic
    pass

@app.get("/users/")
async def read_users():
    users = session.query(User).all()
    return [UserSchema.from_orm(user) for user in users]

@app.get("/teams/")
async def read_teams():
    teams = session.query(Team).all()
    return [TeamSchema.from_orm(team) for team in teams]

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = session.query(User).get(user_id)
    return UserSchema.from_orm(user)

@app.put("/users/{user_id}")
async def update_user(user_id: int, profile: str, tags: List[str]):
    user = session.query(User).get(user_id)
    user.profile = profile
    user.tags = tags
    session.commit()
    return UserSchema.from_orm(user)

@app.post("/teams/")
async def create_team(name: str):
    team = Team(name=name)
    session.add(team)
    session.commit()
    return TeamSchema.from_orm(team)