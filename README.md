# GitHub Insights Ingestion Tool

A modular, type-safe Python CLI tool designed to ingest, validate, and analyze GitHub user profile metrics and repository statistics using **Pydantic v2** and **HTTPX**.

---

## Features

- **Pydantic v2 Models**: Strict validation with custom field validators for GitHub API responses (`UserProfile` & `Repository`).
- **Layered Architecture**: Organized into distinct layers (`core`, `models`, `services`, `utils`).
- **Resilient HTTP Client**: Built with `httpx` featuring timeouts, redirection handling, and standard GitHub API headers.
- **Data Filtering & Ranking**: Automatically filters out forks and ranks source repositories by star count descending.
- **Robust Error Handling**: Graceful error handling for HTTP 404 (user not found), HTTP 403 (rate limiting), network timeouts, and JSON validation issues.
- **Automated Unit Tests**: Built-in test suite verifying data models, edge cases, and ranking logic.
- **Clean Terminal UI**: Structured metrics overview and top-repository breakdown.

---

## Project Structure

```text
github_data_ingestor/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # API URLs, headers, default settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic v2 validation models
│   ├── services/
│   │   ├── __init__.py
│   │   └── github_service.py  # HTTP client & GitHub REST API service
│   └── utils/
│       ├── __init__.py
│       └── presenter.py       # Terminal UI formatting & output
├── tests/
│   ├── __init__.py
│   └── test_models.py         # Unit tests for schemas & business logic
├── main.py                    # Application CLI entry point
├── schemas.py                 # Re-export alias for models
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RonanStack24/github-data-ingestor.git
   cd github-data-ingestor
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows PowerShell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # On Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Execute `main.py` using Python:

```bash
py main.py
```

---

## Running Unit Tests

Run the built-in test suite:

```bash
py -m unittest discover tests
```

---

## Sample Terminal Output

```text
Enter GitHub username (default: 'octocat'): octocat

[i] Ingesting data for user 'octocat'...

======================================================================
                   GITHUB PROFILE INSIGHTS: octocat                   
======================================================================
 * Username     : octocat
 * Display Name : The Octocat
 * Public Repos : 8
 * Followers    : 23,841
 * Profile URL  : https://github.com/octocat
----------------------------------------------------------------------
                   TOP 5 STARRED SOURCE REPOSITORIES                  
----------------------------------------------------------------------
 [1] Spoon-Knife  |  * 14,000 stars  |  Lang: HTML
     Description : This repo is for demonstration purposes only.
     URL         : https://github.com/octocat/Spoon-Knife

 [2] Hello-World  |  * 3,783 stars  |  Lang: Unknown
     Description : My first repository on GitHub!
     URL         : https://github.com/octocat/Hello-World

 [3] octocat.github.io  |  * 1,153 stars  |  Lang: CSS
     Description : No description provided.
     URL         : https://github.com/octocat/octocat.github.io

 [4] hello-worId  |  * 793 stars  |  Lang: Unknown
     Description : My first repository on GitHub.
     URL         : https://github.com/octocat/hello-worId

 [5] git-consortium  |  * 606 stars  |  Lang: Unknown
     Description : This repo is for demonstration purposes only.
     URL         : https://github.com/octocat/git-consortium
======================================================================
```

---

## License

MIT License
