"""
app/core/config.py - Application configuration and constants.
"""

GITHUB_API_BASE_URL: str = "https://api.github.com"
DEFAULT_TIMEOUT_SECONDS: float = 10.0
DEFAULT_USER: str = "octocat"
DEFAULT_HEADERS: dict[str, str] = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "GitHub-Insights-Ingestor",
    "X-GitHub-Api-Version": "2022-11-28",
}
