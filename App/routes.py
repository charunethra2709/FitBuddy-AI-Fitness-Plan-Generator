
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import markdown

from .schemas import UserProfile
from .gemini_generator import generate_fitness_plan
from .gemini_flash_generator import generate_nutrition_tips
from .updated_plan import update_fitness_plan
from .database import SessionLocal, UserPlan


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "Template")
)


# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------
# GENERATE FITNESS PLAN
# ---------------------------------------

@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,

    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    goal: str = Form(...),
    fitness_level: str = Form(...),
    diet: str = Form(...),
    workout_days: int = Form(...),
    medical_conditions: str = Form("")
):

    profile = UserProfile(
        name=name,
        age=age,
        gender=gender,
        goal=goal,
        fitness_level=fitness_level,
        diet=diet,
        workout_days=workout_days,
        medical_conditions=medical_conditions
    )


    # Generate fitness plan
    fitness_plan = generate_fitness_plan(profile)


    # Generate nutrition tips
    nutrition_tips = generate_nutrition_tips(profile)


    # Convert Markdown to HTML
    fitness_plan_html = markdown.markdown(
        fitness_plan,
        extensions=["extra"]
    )


    nutrition_tips_html = markdown.markdown(
        nutrition_tips,
        extensions=["extra"]
    )


    # Save to database
    db = SessionLocal()

    try:

        new_plan = UserPlan(
            name=profile.name,
            age=profile.age,
            gender=profile.gender,
            goal=profile.goal,
            fitness_level=profile.fitness_level,
            diet=profile.diet,
            workout_days=profile.workout_days,
            medical_conditions=profile.medical_conditions,
            fitness_plan=fitness_plan,
            nutrition_tips=nutrition_tips
        )

        db.add(new_plan)
        db.commit()

    finally:

        db.close()


    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "request": request,

            "profile": profile,

            "fitness_plan": fitness_plan_html,

            "fitness_plan_raw": fitness_plan,

            "nutrition_tips": nutrition_tips_html,

            "nutrition_tips_raw": nutrition_tips
        }
    )


# ---------------------------------------
# UPDATE FITNESS PLAN
# ---------------------------------------

@router.post("/update-plan", response_class=HTMLResponse)
async def update_plan(
    request: Request,

    current_plan: str = Form(...),

    feedback: str = Form(...),

    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    goal: str = Form(...),
    fitness_level: str = Form(...),
    diet: str = Form(...),
    workout_days: int = Form(...),
    medical_conditions: str = Form(""),

    nutrition_tips: str = Form("")
):

    profile = UserProfile(
        name=name,
        age=age,
        gender=gender,
        goal=goal,
        fitness_level=fitness_level,
        diet=diet,
        workout_days=workout_days,
        medical_conditions=medical_conditions
    )


    # Ask Gemini to update the plan
    updated_plan = update_fitness_plan(
        current_plan,
        feedback
    )


    # Convert updated Markdown to HTML
    updated_plan_html = markdown.markdown(
        updated_plan,
        extensions=["extra"]
    )


    # Convert nutrition tips back to HTML
    nutrition_tips_html = markdown.markdown(
        nutrition_tips,
        extensions=["extra"]
    )


    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "request": request,

            "profile": profile,

            "fitness_plan": updated_plan_html,

            "fitness_plan_raw": updated_plan,

            "nutrition_tips": nutrition_tips_html,

            "nutrition_tips_raw": nutrition_tips,

            "updated": True
        }
    )


# ---------------------------------------
# VIEW SAVED PLANS
# ---------------------------------------

@router.get("/users", response_class=HTMLResponse)
async def all_users(request: Request):

    db = SessionLocal()

    try:
        users = db.query(UserPlan).all()

        for user in users:
            user.fitness_plan = markdown.markdown(
                user.fitness_plan,
                extensions=["extra"]
            )

            user.nutrition_tips = markdown.markdown(
                user.nutrition_tips,
                extensions=["extra"]
            )

    finally:
        db.close()

    return templates.TemplateResponse(
        request,
        "all_users.html",
        {
            "request": request,
            "users": users
        }
    )