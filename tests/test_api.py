"""
tests/test_api.py - Integration and route tests for FastAPI endpoints.
"""

import unittest
from starlette.testclient import TestClient
from app.server import app


class TestFastAPIEndpoints(unittest.TestCase):
    """Test suite for FastAPI REST API endpoints."""

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check_endpoint(self):
        """Verify root health check endpoint returns 200 OK and valid JSON."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("documentation", data)

    def test_developer_insights_valid_user(self):
        """Verify GET /api/v1/developers/{username} with octocat."""
        response = self.client.get("/api/v1/developers/octocat?top_limit=3")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["profile"]["login"], "octocat")
        self.assertIn("top_repositories", data)
        self.assertLessEqual(len(data["top_repositories"]), 3)

    def test_developer_insights_nonexistent_user(self):
        """Verify GET /api/v1/developers/{username} for unknown user returns 404."""
        response = self.client.get("/api/v1/developers/non_existent_user_xyz_123_456_789")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
