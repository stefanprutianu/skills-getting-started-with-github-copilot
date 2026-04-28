import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# Create a test client
client = TestClient(app)

# Original activities data for resetting
ORIGINAL_ACTIVITIES = {
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
    "Music Band": {
        "description": "Join our concert band and perform at school events",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["ryan@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific discoveries",
        "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 22,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu", "chloe@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test"""
    global activities
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES.copy())

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=new@student.edu")
    assert response.status_code == 200
    assert "Signed up new@student.edu for Chess Club" in response.json()["message"]
    
    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "new@student.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@test.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered michael@mergington.edu from Chess Club" in response.json()["message"]
    
    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@test.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
