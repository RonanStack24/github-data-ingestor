"""
app/server.py - FastAPI Application Factory and Server Entry Point.
"""

import sys
from pathlib import Path

# Ensure root directory is in sys.path for direct execution (e.g., py app/server.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import developer_router

# Initialize FastAPI application with OpenAPI metadata
app = FastAPI(
    title="GitHub Insights Ingestion API",
    description="A high-performance REST API to ingest, validate, and analyze GitHub user profiles and repositories.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend applications (React, Vue, mobile apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(developer_router)


@app.get("/", tags=["Health"])
def health_check():
    """
    Root health check endpoint providing service status and documentation links.
    """
    return {
        "status": "healthy",
        "service": "GitHub Insights Ingestion API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "developer_insights": "/api/v1/developers/{username}",
        },
    }


if __name__ == "__main__":
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
