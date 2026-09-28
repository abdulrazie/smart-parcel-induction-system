"""
Main FastAPI Application Entrypoint
-----------------------------------
This file creates the FastAPI app instance, registers middleware, and defines
initial health check and status routes.

Key Concepts:
1. `FastAPI(title=..., version=...)`: Automatically generates interactive Swagger UI at `/docs`
   and ReDoc at `/redoc`.
2. Middleware: Cross-Origin Resource Sharing (CORS) allows the frontend to communicate with
   the backend even if hosted on different local ports during development.
3. Health check: Standard DevOps endpoint to monitor whether the server and database are healthy.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import get_settings
from app.database import get_db

# Load settings
settings = get_settings()

# Initialize FastAPI instance
app = FastAPI(
    title=settings.APP_NAME,
    description="Smart Parcel Induction & Pickup Management System for University Mailrooms",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI documentation
    redoc_url="/redoc",    # ReDoc alternative documentation
)

# Configure CORS (Cross-Origin Resource Sharing)
# In production, specify exact origins; during local development, allow all origins for ease of testing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def read_root():
    """
    Root Welcome Endpoint.
    Provides basic app metadata and quick links to API documentation.
    """
    return {
        "message": f"Welcome to the {settings.APP_NAME} API",
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health"
    }


@app.get(f"{settings.API_PREFIX}/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """
    Health Check Endpoint.
    Verifies that both the FastAPI server and the database connection are operational.
    """
    try:
        # Run a lightweight query to test active DB connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "app_name": settings.APP_NAME,
        "database": db_status
    }
