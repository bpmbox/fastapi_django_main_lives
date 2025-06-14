from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    profile = Column(String)
    team_id = Column(Integer)
    tags = Column(String)

    def __repr__(self):
        return f"User(username={self.username}, profile={self.profile}, team_id={self.team_id}, tags={self.tags})"