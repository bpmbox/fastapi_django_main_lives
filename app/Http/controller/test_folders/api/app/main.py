from fastapi import FastAPI
from routers import user, team, knowledge

app = FastAPI()

app.include_router(user.router")
app.include_router(team.router")
app.include_router(knowledge.router")