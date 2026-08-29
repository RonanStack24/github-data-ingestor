"""
tests/test_models.py - Unit tests for Pydantic models and validators.
"""

import unittest
from pydantic import ValidationError
from app.models.schemas import Repository, UserProfile
from app.services.github_service import process_repositories


class TestGitHubSchemas(unittest.TestCase):
    """Test suite for UserProfile and Repository Pydantic schemas."""

    def test_user_profile_valid(self):
        """Verify valid user profile payload parses successfully."""
        data = {
            "login": "octocat",
            "name": "The Octocat",
            "public_repos": 8,
            "followers": 23000,
            "html_url": "https://github.com/octocat",
        }
        profile = UserProfile.model_validate(data)
        self.assertEqual(profile.login, "octocat")
        self.assertEqual(profile.name, "The Octocat")
        self.assertEqual(profile.public_repos, 8)
        self.assertEqual(profile.followers, 23000)

    def test_user_profile_null_name_defaults_to_na(self):
        """Verify null/empty display name defaults to 'N/A'."""
        data = {
            "login": "ghost",
            "name": None,
            "public_repos": 0,
            "followers": 0,
            "html_url": "https://github.com/ghost",
        }
        profile = UserProfile.model_validate(data)
        self.assertEqual(profile.name, "N/A")

    def test_repository_null_language_defaults_to_unknown(self):
        """Verify null/empty language defaults to 'Unknown'."""
        data = {
            "name": "docs",
            "description": "Documentation repo",
            "stargazers_count": 50,
            "fork": False,
            "language": None,
            "html_url": "https://github.com/octocat/docs",
        }
        repo = Repository.model_validate(data)
        self.assertEqual(repo.language, "Unknown")
        self.assertFalse(repo.fork)

    def test_repository_filter_and_sorting(self):
        """Verify process_repositories filters forks and sorts by stars descending."""
        repo1 = Repository(
            name="repo1", stargazers_count=10, fork=False, html_url="https://github.com/user/repo1"
        )
        repo2_fork = Repository(
            name="repo2", stargazers_count=1000, fork=True, html_url="https://github.com/user/repo2"
        )
        repo3 = Repository(
            name="repo3", stargazers_count=50, fork=False, html_url="https://github.com/user/repo3"
        )

        filtered_and_sorted = process_repositories([repo1, repo2_fork, repo3])
        
        # Must exclude fork repo2
        self.assertEqual(len(filtered_and_sorted), 2)
        # Must sort descending: repo3 (50 stars) first, then repo1 (10 stars)
        self.assertEqual(filtered_and_sorted[0].name, "repo3")
        self.assertEqual(filtered_and_sorted[1].name, "repo1")


if __name__ == "__main__":
    unittest.main()
