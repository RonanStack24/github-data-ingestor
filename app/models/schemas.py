"""
app/models/schemas.py - Pydantic Data Models for GitHub API Entities and API Responses.

Defines validation schemas for GitHub user profiles, repositories, and
FastAPI response models using Pydantic v2.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


class UserProfile(BaseModel):
    """
    Schema representing a GitHub user's public profile.
    
    Attributes:
        login (str): The unique GitHub handle / username.
        name (Optional[str]): The user's display name, defaults to 'N/A' if null/empty.
        public_repos (int): Count of public repositories owned by the user.
        followers (int): Count of users following this profile.
        html_url (HttpUrl): Direct web URL to the GitHub profile.
    """
    login: str = Field(
        ...,
        description="GitHub username/handle"
    )
    name: Optional[str] = Field(
        default="N/A",
        description="Full name of the user or 'N/A' if not provided"
    )
    public_repos: int = Field(
        ...,
        ge=0,
        description="Total number of public repositories"
    )
    followers: int = Field(
        ...,
        ge=0,
        description="Total number of followers"
    )
    html_url: HttpUrl = Field(
        ...,
        description="Public URL for the user profile"
    )

    @field_validator("name", mode="before")
    @classmethod
    def default_name_if_none(cls, v: Optional[str]) -> str:
        """Handle null/empty values from GitHub API by defaulting to 'N/A'."""
        if v is None or not str(v).strip():
            return "N/A"
        return str(v).strip()


class Repository(BaseModel):
    """
    Schema representing a GitHub repository.
    
    Attributes:
        name (str): Repository name.
        description (Optional[str]): Repository summary or description.
        stargazers_count (int): Total number of stars/stargazers.
        fork (bool): True if the repository is a fork, False if it is a source repository.
        language (Optional[str]): Dominant programming language, defaults to 'Unknown'.
        html_url (HttpUrl): Direct web URL to the repository.
    """
    name: str = Field(
        ...,
        description="Name of the repository"
    )
    description: Optional[str] = Field(
        default=None,
        description="Brief description of the repository"
    )
    stargazers_count: int = Field(
        default=0,
        ge=0,
        description="Number of stars received"
    )
    fork: bool = Field(
        ...,
        description="Indicates whether this repository is a fork"
    )
    language: Optional[str] = Field(
        default="Unknown",
        description="Primary programming language"
    )
    html_url: HttpUrl = Field(
        ...,
        description="Public URL for the repository"
    )

    @field_validator("language", mode="before")
    @classmethod
    def default_language_if_none(cls, v: Optional[str]) -> str:
        """Handle null/empty language values from GitHub API by defaulting to 'Unknown'."""
        if v is None or not str(v).strip():
            return "Unknown"
        return str(v).strip()


class DeveloperInsightsResponse(BaseModel):
    """
    Schema representing the aggregated API response for a GitHub developer.
    """
    profile: UserProfile = Field(
        ...,
        description="Detailed public profile of the developer"
    )
    total_source_repos: int = Field(
        ...,
        ge=0,
        description="Total count of original non-forked repositories"
    )
    top_repositories: List[Repository] = Field(
        default_factory=list,
        description="Top starred non-forked repositories"
    )
    primary_languages: List[str] = Field(
        default_factory=list,
        description="List of detected programming languages across source repos"
    )
