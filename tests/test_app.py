import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesAPI:
    """Test cases for the activities API endpoints"""

    def test_get_activities(self):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

        # Check that each activity has the required fields
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_specific_activity_structure(self):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()

        # Test with Chess Club which has participants
        chess_club = data.get("Chess Club")
        assert chess_club is not None
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]

    def test_signup_successful(self):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Football Team/signup",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "test@example.com" in data["message"]
        assert "Football Team" in data["message"]

        # Verify the participant was added
        response = client.get("/activities")
        activities = response.json()
        football_team = activities["Football Team"]
        assert "test@example.com" in football_team["participants"]

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/NonExistent Activity/signup",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_signed_up(self):
        """Test signup when student is already signed up"""
        # First signup
        client.post(
            "/activities/Basketball Club/signup",
            json={"email": "duplicate@example.com"}
        )

        # Try to signup again
        response = client.post(
            "/activities/Basketball Club/signup",
            json={"email": "duplicate@example.com"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_activity_full(self):
        """Test signup when activity is at max capacity"""
        # Fill up the Art Club (max 10 participants)
        for i in range(10):
            client.post(
                "/activities/Art Club/signup",
                json={"email": f"student{i}@example.com"}
            )

        # Try to add one more
        response = client.post(
            "/activities/Art Club/signup",
            json={"email": "overflow@example.com"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Activity is full" in data["detail"]

    def test_remove_participant_successful(self):
        """Test successful removal of a participant"""
        # First add a participant
        client.post(
            "/activities/Volleyball Team/signup",
            json={"email": "remove@example.com"}
        )

        # Now remove them
        response = client.delete(
            "/activities/Volleyball Team/participants",
            params={"email": "remove@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "remove@example.com" in data["message"]
        assert "Volleyball Team" in data["message"]

        # Verify they were removed
        response = client.get("/activities")
        activities = response.json()
        volleyball_team = activities["Volleyball Team"]
        assert "remove@example.com" not in volleyball_team["participants"]

    def test_remove_participant_activity_not_found(self):
        """Test removing participant from non-existent activity"""
        response = client.delete(
            "/activities/NonExistent Activity/participants",
            params={"email": "test@example.com"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_found(self):
        """Test removing participant who is not signed up"""
        response = client.delete(
            "/activities/Swimming Club/participants",
            params={"email": "notsignedup@example.com"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_root_redirect(self):
        """Test that root endpoint redirects to static index"""
        response = client.get("/")
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers.get("location", "")