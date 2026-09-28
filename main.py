"""
Project Launcher Script
-----------------------
This file provides a direct entrypoint for running the application.

You can start the server in two ways:
    1. Using this script directly:
       python main.py

    2. Using Uvicorn CLI directly (standard in production):
       uvicorn app.main:app --reload --port 8000
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting Smart Parcel Induction System...")
    print("Interactive Swagger Documentation available at: http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
