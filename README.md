# GitHub Insights Ingestion Tool & REST API

A modular, type-safe Python backend tool & REST API designed to ingest, validate, and analyze GitHub user profile metrics and repository statistics using **FastAPI**, **Pydantic v2**, and **HTTPX**.

---

## Features

- **FastAPI REST API**: High-performance endpoints with automatic interactive documentation (Swagger UI).
- **Pydantic v2 Models**: Strict validation with custom field validators for GitHub API responses (`UserProfile` & `Repository`).
- **Layered Architecture**: Clean separation into `core`, `models`, `services`, `api`, and `utils`.
- **Resilient HTTP Client**: Built with `httpx` featuring timeouts, redirection handling, and standard GitHub API headers.
- **Data Filtering & Ranking**: Automatically filters out forks and ranks source repositories by star count descending.
- **Robust Error Handling**: Graceful handling for HTTP 404, HTTP 403 (rate limiting), network timeouts, and malformed data.
- **Automated Test Suite**: Unit and integration tests covering models, services, and REST API endpoints.

---

## Project Structure

```text
github_data_ingestor/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py       # FastAPI REST API routes
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # API URLs, headers, default settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic v2 validation & response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── github_service.py  # HTTP client & GitHub REST API service
│   ├── utils/
│   │   ├── __init__.py
│   │   └── presenter.py       # Terminal UI formatting & output
│   └── server.py              # FastAPI application server entry point
├── tests/
│   ├── __init__.py
│   ├── test_models.py         # Unit tests for schemas & business logic
│   └── test_api.py            # Integration tests for FastAPI endpoints
├── main.py                    # CLI application entry point
├── schemas.py                 # Re-export alias for models
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone -b feature/fastapi-integration https://github.com/RonanStack24/github-data-ingestor.git
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

## Usage

### Option 1: Run as a REST API (FastAPI)

Start the Uvicorn ASGI server:

```bash
py app/server.py
# or
py -m uvicorn app.server:app --reload
```

Once running, visit:
- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **API Endpoint**: `http://127.0.0.1:8000/api/v1/developers/octocat`

#### Example API Response (`GET /api/v1/developers/octocat`):

```json
{
  "profile": {
    "login": "octocat",
    "name": "The Octocat",
    "public_repos": 8,
    "followers": 23841,
    "html_url": "https://github.com/octocat"
  },
  "total_source_repos": 8,
  "top_repositories": [
    {
      "name": "Spoon-Knife",
      "description": "This repo is for demonstration purposes only.",
      "stargazers_count": 14000,
      "fork": false,
      "language": "HTML",
      "html_url": "https://github.com/octocat/Spoon-Knife"
    }
  ],
  "primary_languages": [
    "HTML",
    "CSS"
  ]
}
```

---

### Option 2: Run as a CLI Terminal Tool

```bash
py main.py
```

---

## Running Unit & Integration Tests

```bash
py -m unittest discover tests
```

---

## License

MIT License
