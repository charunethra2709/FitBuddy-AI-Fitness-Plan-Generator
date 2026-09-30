from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str
    age: int
    gender: str
    goal: str
    fitness_level: str
    diet: str
    workout_days: int
    medical_conditions: str = ""