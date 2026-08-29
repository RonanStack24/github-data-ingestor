"""
app/services/github_service.py - Service layer for communicating with the GitHub REST API.
"""

from typing import List, Optional
import httpx
from pydantic import ValidationError

from app.core.config import (
    DEFAULT_HEADERS,
    DEFAULT_TIMEOUT_SECONDS,
    GITHUB_API_BASE_URL,
)
from app.models.schemas import Repository, UserProfile


def create_github_client() -> httpx.Client:
    """
    Instantiate an HTTP client configured for GitHub REST API requests.

    Returns:
        httpx.Client: Configured HTTP client with standard timeouts and headers.
    """
    return httpx.Client(
        base_url=GITHUB_API_BASE_URL,
        headers=DEFAULT_HEADERS,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        follow_redirects=True,
    )


def fetch_user_profile(client: httpx.Client, username: str) -> Optional[UserProfile]:
    """
    Fetch and validate the GitHub public user profile.

    Args:
        client (httpx.Client): Active HTTP client session.
        username (str): The GitHub username to look up.

    Returns:
        Optional[UserProfile]: Validated UserProfile instance, or None if not found / error.
    """
    endpoint = f"/users/{username}"
    try:
        response = client.get(endpoint)
        if response.status_code == 404:
            print(f"\n[!] Error: User '{username}' was not found on GitHub (HTTP 404).")
            return None

        response.raise_for_status()
        raw_data = response.json()
        return UserProfile.model_validate(raw_data)

    except httpx.HTTPStatusError as err:
        if err.response.status_code == 403 and "rate limit" in err.response.text.lower():
            print("\n[!] API Error: GitHub API rate limit exceeded. Please try again later.")
        else:
            print(f"\n[!] HTTP Error {err.response.status_code}: {err.response.text}")
        return None
    except httpx.TimeoutException:
        print(f"\n[!] Network Error: Request timed out while fetching profile for '{username}'.")
        return None
    except httpx.RequestError as err:
        print(f"\n[!] Network Error: Failed to connect to GitHub API: {err}")
        return None
    except ValidationError as err:
        print(f"\n[!] Validation Error: Failed to parse UserProfile data for '{username}':")
        print(err)
        return None


def fetch_user_repositories(client: httpx.Client, username: str) -> List[Repository]:
    """
    Fetch up to 100 updated repositories for a user and validate them against Repository schema.

    Args:
        client (httpx.Client): Active HTTP client session.
        username (str): The GitHub username whose repos should be retrieved.

    Returns:
        List[Repository]: List of successfully validated Repository instances.
    """
    endpoint = f"/users/{username}/repos"
    params = {
        "per_page": 100,
        "sort": "updated",
    }
    try:
        response = client.get(endpoint, params=params)
        response.raise_for_status()
        raw_repos = response.json()

        validated_repos: List[Repository] = []
        for index, item in enumerate(raw_repos):
            try:
                repo_model = Repository.model_validate(item)
                validated_repos.append(repo_model)
            except ValidationError as err:
                print(f"[!] Warning: Skipping repository at index {index} due to validation error: {err}")

        return validated_repos

    except httpx.TimeoutException:
        print(f"\n[!] Network Error: Request timed out while fetching repositories for '{username}'.")
        return []
    except httpx.RequestError as err:
        print(f"\n[!] Network Error: Failed to connect to GitHub API: {err}")
        return []
    except httpx.HTTPStatusError as err:
        print(f"\n[!] HTTP Error {err.response.status_code} while fetching repos: {err.response.text}")
        return []


def process_repositories(repos: List[Repository]) -> List[Repository]:
    """
    Filter out forked repositories and sort source repositories by stargazers_count descending.

    Args:
        repos (List[Repository]): Raw validated repository list.

    Returns:
        List[Repository]: Filtered and sorted source repositories.
    """
    # Exclude forks (keep only source repos)
    source_repos = [repo for repo in repos if not repo.fork]

    # Sort descending by star count
    return sorted(source_repos, key=lambda repo: repo.stargazers_count, reverse=True)
