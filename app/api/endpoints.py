"""
app/api/endpoints.py - REST API Route handlers for developer insights.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.models.schemas import DeveloperInsightsResponse
from app.services.github_service import (
    create_github_client,
    fetch_user_profile,
    fetch_user_repositories,
    process_repositories,
)

router = APIRouter(prefix="/api/v1/developers", tags=["Developers"])


@router.get(
    "/{username}",
    response_model=DeveloperInsightsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get GitHub Developer Profile & Insights",
    description="Fetches public metrics, filters out forks, and returns ranked top repositories.",
)
def get_developer_insights(
    username: str,
    top_limit: int = Query(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of top starred repositories to return",
    ),
):
    """
    Retrieve developer profile metrics and top ranked original repositories.
    """
    with create_github_client() as client:
        profile = fetch_user_profile(client, username)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"GitHub user '{username}' was not found or could not be retrieved.",
            )

        all_repos = fetch_user_repositories(client, username)
        source_repos = process_repositories(all_repos)
        top_repos = source_repos[:top_limit]

        # Extract unique detected languages (excluding 'Unknown')
        languages = list(
            dict.fromkeys(
                repo.language
                for repo in source_repos
                if repo.language and repo.language != "Unknown"
            )
        )

        return DeveloperInsightsResponse(
            profile=profile,
            total_source_repos=len(source_repos),
            top_repositories=top_repos,
            primary_languages=languages,
        )
