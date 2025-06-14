from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.app.models import Base
from api.app.routers import user_router, team_router

app = FastAPI()

engine = create_engine('sqlite:///api.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")

app.include_router(user_router)
app.include_router(team_router)