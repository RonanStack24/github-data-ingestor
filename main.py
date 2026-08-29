"""
main.py - GitHub User Profile and Repository Ingestion CLI Tool.

This module interacts with the GitHub REST API (v3 / 2022-11-28) to fetch public
profile data and repository metrics for a given user, applying strict Pydantic v2
validation, filtering, and formatted terminal output.
"""

import sys
from typing import List, Optional
import httpx
from pydantic import ValidationError

from schemas import Repository, UserProfile


# Base constants for GitHub API communication
GITHUB_API_BASE_URL = "https://api.github.com"
DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_USER = "octocat"
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "GitHub-Insights-Ingestor",
    "X-GitHub-Api-Version": "2022-11-28",
}


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


def display_insights(profile: UserProfile, top_repos: List[Repository]) -> None:
    """
    Render a clean, formatted terminal summary of profile metrics and top repositories.

    Args:
        profile (UserProfile): Validated user profile model.
        top_repos (List[Repository]): List of top starred source repositories (up to 5).
    """
    border_width = 70
    print("\n" + "=" * border_width)
    print(f" GITHUB PROFILE INSIGHTS: {profile.login}".center(border_width))
    print("=" * border_width)

    # Display User Profile Details
    print(f" * Username     : {profile.login}")
    print(f" * Display Name : {profile.name}")
    print(f" * Public Repos : {profile.public_repos:,}")
    print(f" * Followers    : {profile.followers:,}")
    print(f" * Profile URL  : {profile.html_url}")
    print("-" * border_width)

    # Display Top Starred Source Repositories
    print(f" TOP {len(top_repos)} STARRED SOURCE REPOSITORIES".center(border_width))
    print("-" * border_width)

    if not top_repos:
        print(" No public source repositories found for this account.")
    else:
        for rank, repo in enumerate(top_repos, start=1):
            desc = repo.description if repo.description else "No description provided."
            # Truncate overly long descriptions for neat terminal layout
            if len(desc) > 65:
                desc = desc[:62] + "..."

            print(f" [{rank}] {repo.name}  |  * {repo.stargazers_count:,} stars  |  Lang: {repo.language}")
            print(f"     Description : {desc}")
            print(f"     URL         : {repo.html_url}")
            if rank < len(top_repos):
                print()

    print("=" * border_width + "\n")


def main() -> None:
    """
    Main entry point for the GitHub data ingestion CLI tool.
    """
    try:
        user_input = input(f"Enter GitHub username (default: '{DEFAULT_USER}'): ").strip()
        username = user_input if user_input else DEFAULT_USER

        print(f"\n[i] Ingesting data for user '{username}'...")

        with create_github_client() as client:
            # 1. Fetch & validate user profile
            profile = fetch_user_profile(client, username)
            if not profile:
                sys.exit(1)

            # 2. Fetch & validate repositories
            all_repos = fetch_user_repositories(client, username)

            # 3. Filter out forks and rank by star count
            source_repos = process_repositories(all_repos)
            top_5_repos = source_repos[:5]

            # 4. Present summary
            display_insights(profile, top_5_repos)

    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
