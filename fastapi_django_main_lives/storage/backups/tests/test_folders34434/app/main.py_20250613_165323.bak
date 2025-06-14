from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme
from sqlalchemy.orm import sessionmaker
from app.routers import users, teams, profiles
from app.models import Base

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown_event():
    engine.dispose()

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(profiles.router)