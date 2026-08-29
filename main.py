"""
main.py - GitHub User Profile and Repository Ingestion CLI Tool.

CLI entry point coordinating the GitHub ingestion pipeline.
"""

import sys
from app.core import DEFAULT_USER
from app.services import (
    create_github_client,
    fetch_user_profile,
    fetch_user_repositories,
    process_repositories,
)
from app.utils import display_insights


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
