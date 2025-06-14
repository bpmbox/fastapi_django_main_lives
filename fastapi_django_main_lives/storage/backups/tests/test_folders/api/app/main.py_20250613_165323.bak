from fastapi import FastAPI
from routers import user, team
from db import engine

app = FastAPI()

app.include_router(user.router)
app.include_router(team.router)

@app.on_event("startup")
async def startup():
    await engine.connect()

@app.on_event("shutdown")
async def shutdown():
    await engine.disconnect()