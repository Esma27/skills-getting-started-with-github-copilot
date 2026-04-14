"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
        "Football Team": {
        "description": "Train and compete in football matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Practice basketball and join tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting and creative arts",
        "schedule": "Fridays, 2:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": []
    },
    "Music Band": {
        "description": "Play instruments and perform music",
        "schedule": "Wednesdays, 3:00 PM - 5:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Math Club": {
        "description": "Solve math problems and compete",
        "schedule": "Mondays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and learn science",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Volleyball Team": {
        "description": "Practice volleyball skills and compete in matches",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Swimming Club": {
        "description": "Improve swimming technique and participate in relays",
        "schedule": "Wednesdays and Saturdays, 4:30 PM - 6:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Drama Club": {
        "description": "Rehearse plays and perform theater productions",
        "schedule": "Mondays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Creative Writing Workshop": {
        "description": "Write stories, poems, and scripts with feedback",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": []
    },
    "Robotics Club": {
        "description": "Design robots and compete in engineering challenges",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["lila@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare arguments and compete in debate tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
