from fastapi import FastAPI
from api.routers.user import router as user_router
from api.routers.team import router as team_router

app = FastAPI()

app.include_router(user_router)
app.include_router(team_router)