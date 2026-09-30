from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(50))
    goal = Column(String(100))
    fitness_level = Column(String(50))
    diet = Column(String(50))
    workout_days = Column(Integer)
    medical_conditions = Column(Text)

    fitness_plan = Column(Text)
    nutrition_tips = Column(Text)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)