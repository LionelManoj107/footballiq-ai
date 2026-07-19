import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./footballiq.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    city = Column(String)


class DrillSession(Base):
    __tablename__ = "drill_sessions"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    drill_type = Column(String)
    video_path = Column(String)


class SkillScore(Base):
    __tablename__ = "skill_scores"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("drill_sessions.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    drill_type = Column(String)
    category = Column(String)   # control | technique | balance | accuracy
    score = Column(Float)       # 0-100


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()
