# 🏋️ FitBuddy

## AI Fitness Plan Generator

FitBuddy is an AI-powered fitness planning web application built using FastAPI, Gemini AI, Jinja2 and SQLite.

## Features

- User fitness profile
- AI-generated 7-day fitness plan
- Table-based workout plan
- General nutrition information
- Plan update using user feedback
- SQLite database
- Saved fitness plans
- Saved plans viewing page

## Technologies Used

- Python
- FastAPI
- Gemini API
- Google GenAI SDK
- Jinja2
- SQLAlchemy
- SQLite
- HTML
- CSS

## Project Structure

```text
FitBuddy/
│
├── App/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── schemas.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
│
├── Template/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── fitbuddy.db