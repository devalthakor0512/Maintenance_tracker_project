from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, index=True)

    members = relationship("User", secondary=team_members, backref="teams")
