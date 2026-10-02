#!/usr/bin/env python3
"""
CampusStay - Hostel Management System
One-click Local Development & Presentation Server
"""

import sys
import time
import webbrowser
import uvicorn
from pathlib import Path

# Add backend directory to Python path
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))


def main():
    print("=" * 60)
    print("  CampusStay - Enterprise Hostel Management System")
    print("  FastAPI Backend + Nginx/Vanilla UI + Supabase PostgreSQL")
    print("=" * 60)
    print("\n[+] Starting FastAPI server at http://127.0.0.1:8000 ...")
    print("[+] Dashboard available at: http://127.0.0.1:8000/dashboard")
    print("[+] Swagger API documentation at: http://127.0.0.1:8000/docs")
    print("[+] Healthcheck endpoint: http://127.0.0.1:8000/health")
    print("\nPress CTRL+C to stop the server.\n")

    # Automatically open default browser after a brief delay
    time.sleep(1.5)
    try:
        webbrowser.open("http://127.0.0.1:8000/dashboard")
    except Exception:
        pass

    # Launch Uvicorn server
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, app_dir=str(BACKEND_DIR))


if __name__ == "__main__":
    main()
