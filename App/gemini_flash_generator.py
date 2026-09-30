import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_nutrition_tips(profile):

    prompt = f"""
Give simple and practical general nutrition information.

Goal: {profile.goal}
Fitness Level: {profile.fitness_level}
Diet: {profile.diet}
Workout Days: {profile.workout_days}

Use these headings:

### Suitable Foods
### Protein Sources
### Healthy Meal Suggestions
### Hydration
### General Healthy Eating Tips

Use normal Markdown bullet points.

Do not use escaped characters such as \\*.

Keep the suggestions age-appropriate and general.
Do not provide calorie targets, restrictive diets, supplements,
or medical treatment advice.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("Nutrition Gemini API Error:", e)

        return "Nutrition tips are temporarily unavailable."