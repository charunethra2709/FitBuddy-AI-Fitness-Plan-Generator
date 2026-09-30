from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator"
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "FitBuddy is running"}