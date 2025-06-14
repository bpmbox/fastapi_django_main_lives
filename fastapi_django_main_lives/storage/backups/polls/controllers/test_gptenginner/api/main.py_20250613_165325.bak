from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import List

app = FastAPI()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    profile = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", backref="users")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

engine = create_async_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.on_event("startup")
async def startup():
    async with async_session() as session:
        await session.execute("PRAGMA foreign_keys=ON")

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

class UserSchema(BaseModel):
    username: str
    password: str
    profile: str
    team_id: int

class TeamSchema(BaseModel):
    name: str

@app.post("/register")
async def register_user(user: UserSchema):
    async with async_session() as session:
        existing_user = await session.execute(User.__table__.select().where(User.username == user.username))
        if existing_user.scalar():
            return JSONResponse(status_code=400, content={"error": "Username already exists"})
        new_user = User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id)
        session.add(new_user)
        await session.commit()
        return JSONResponse(status_code=201, content={"message": "User created successfully"})

@app.post("/login")
async def login_user(username: str, password: str):
    async with async_session() as session:
        user = await session.execute(User.__table__.select().where(User.username == username))
        user = user.scalar()
        if not user or user.password != password:
            return JSONResponse(status_code=401, content={"error": "Invalid username or password"})
        return JSONResponse(status_code=200, content={"message": "Logged in successfully"})

@app.get("/teams/")
async def get_teams():
    async with async_session() as session:
        teams = await session.execute(Team.__table__.select())
        teams = teams.scalars().all()
        return JSONResponse(status_code=200, content=[{"id": team.id, "name": team.name} for team in teams])

@app.post("/teams/")
async def create_team(team: TeamSchema):
    async with async_session() as session:
        new_team = Team(name=team.name)
        session.add(new_team)
        await session.commit()
        return JSONResponse(status_code=201, content={"message": "Team created successfully"})

@app.get("/users/")
async def get_users():
    async with async_session() as session:
        users = await session.execute(User.__table__.select())
        users = users.scalars().all()
        return JSONResponse(status_code=200, content=[{"id": user.id, "username": user.username, "profile": user.profile} for user in users])

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with async_session() as session:
        user = await session.execute(User.__table__.select().where(User.id == user_id))
        user = user.scalar()
        if not user:
            return JSONResponse(status_code=404, content={"error": "User not found"})
        return JSONResponse(status_code=200, content={"username": user.username, "profile": user.profile, "team_id": user.team_id})

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserSchema):
    async with async_session() as session:
        user_db = await session.execute(User.__table__.select().where(User.id == user_id))
        user_db = user_db.scalar()
        if not user_db:
            return JSONResponse(status_code=404, content={"error": "User not found"})
        user_db.username = user.username
        user_db.profile = user.profile
        user_db.team_id = user.team_id
        await session.commit()
        return JSONResponse(status_code=200, content={"message": "User updated successfully"})

@app.get("/search")
async def search_users(q: str):
    async with async_session() as session:
        users = await session.execute(User.__table__.select().where(User.profile.like(f"%{q}%")))
        users = users.scalars().all()
        return JSONResponse(status_code=200, content=[{"id": user.id, "username": user.username, "profile": user.profile} for user in users])