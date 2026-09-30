import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def update_fitness_plan(current_plan, feedback):

    prompt = f"""
Update the following fitness plan based on the user's feedback.

CURRENT FITNESS PLAN:
{current_plan}

USER FEEDBACK:
{feedback}

Return the updated plan as a Markdown table.

Use exactly these columns:

| Day | Workout | Exercises | Sets/Reps | Rest |

Create one row for each day.

Keep the suggestions general, age-appropriate, practical, and safe.
Do not recommend extreme exercise, restrictive diets, calorie targets,
supplements, or changes to prescribed medical treatment.

Return only the updated Markdown table.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Update Plan Gemini Error:", e)

        return (
            "The plan could not be updated right now. "
            "Please try again later."
        )