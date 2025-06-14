from fastapi import FastAPI
from app.main import app
from app.routers import users, teams

app.include_router(users.router)
app.include_router(teams.router)