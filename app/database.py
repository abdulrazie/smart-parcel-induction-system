"""
Database Connection & Session Management
----------------------------------------
This module initializes the SQLAlchemy connection to the database.

Key Concepts:
1. Engine: The core interface to the database. It manages a pool of connections.
2. SessionLocal: A factory for creating new Session objects. Each HTTP request gets its own session.
3. Base: The declarative base class that all ORM models inherit from so SQLAlchemy knows about our tables.
4. get_db(): A dependency generator. In FastAPI, `Depends(get_db)` provides a fresh database session
   for each request and guarantees it is closed when the request finishes, preventing connection leaks.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import get_settings

# Retrieve current settings (reads DATABASE_URL from .env)
settings = get_settings()

# Check if using SQLite (which requires special threading flags)
# SQLite by default prevents sharing connections across different threads.
# FastAPI uses multithreading for concurrent requests, so for SQLite we set check_same_thread=False.
# For PostgreSQL, connect_args is not needed.
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create the SQLAlchemy Engine
# `echo=settings.DEBUG` prints all generated SQL queries to the terminal when DEBUG=True.
# This is extremely useful for learning and debugging SQL in development!
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG
)

# Create a customized Session class
# - autocommit=False ensures transactions are only committed when we explicitly call db.commit().
# - autoflush=False prevents automatic flush before queries unless we choose to.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session to API route handlers.

    Usage in a router:
        @router.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...

    The `yield` statement passes the session to the route.
    The `finally` block guarantees `db.close()` runs even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
