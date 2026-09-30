import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_fitness_plan(profile):

    prompt = f"""
Create a simple and age-appropriate 7-day fitness plan.

Name: {profile.name}
Age: {profile.age}
Gender: {profile.gender}
Goal: {profile.goal}
Fitness Level: {profile.fitness_level}
Diet: {profile.diet}
Workout Days: {profile.workout_days}
Medical Conditions: {profile.medical_conditions}

Return the fitness plan ONLY as a Markdown table.

Use exactly these columns:

| Day | Workout | Exercises | Sets/Reps | Rest |

Create one row for each day.

For rest days, write "Rest Day" in the Workout column.

Keep the exercises general, age-appropriate, and safe.
Do not recommend extreme exercise, restrictive diets, calorie targets,
supplements, or changes to prescribed medical treatment.

If medical conditions are provided, advise the user to consult
a qualified healthcare professional before changing their exercise routine.

Keep the table clear and easy to understand.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini API Error:", e)

        return (
            "Gemini is temporarily unavailable. "
            "Please try generating the plan again later."
        )