"""
app/utils/presenter.py - Terminal rendering and display utilities.
"""

from typing import List
from app.models.schemas import Repository, UserProfile


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
