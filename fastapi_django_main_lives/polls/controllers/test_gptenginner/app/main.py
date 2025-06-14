from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base
from app.routers import users, teams

app = FastAPI()

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    session.close()