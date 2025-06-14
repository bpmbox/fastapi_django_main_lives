from fastapi import FastAPI
from app.routers import users, teams

app = FastAPI()

app.include_router(users.router)
app.include_router(teams.router)