from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    profile = Column(String)
    tags = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", backref="users")

    @classmethod
    def exists(cls, username, db):
        return db.query(cls).filter(cls.username == username).first() is not None

    @classmethod
    def authenticate(cls, username, password, db):
        user = db.query(cls).filter(cls.username == username).first()
        if user and user.password == password:
            return user
        return None

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)