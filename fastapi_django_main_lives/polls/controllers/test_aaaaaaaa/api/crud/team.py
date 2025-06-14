from api.models import Team
from api.schemas import TeamSchema

def create_team(name: str):
    team = Team(name=name)
    session.add(team)
    session.commit()
    return team