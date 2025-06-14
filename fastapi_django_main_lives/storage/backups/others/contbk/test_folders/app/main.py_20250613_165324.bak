from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app.models.user import User
from app.models.team import Team
from app.schema.user import UserSchema
from app.schema.team import TeamSchema
from app.crud.user import crud_user
from app.crud.team import crud_team
from app.routers.user import router as user_router
from app.routers.team import router as team_router

app = FastAPI()

engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown_event():
    engine.dispose()

app.include_router(user_router)
app.include_router(team_router)