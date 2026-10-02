# ==============================================================================
# CampusStay Enterprise Hostel Management System - Core REST API
# Principal Architect & Backend Lead: Ananya (@Ananya5182)
# Issue: HMS-1 (FastAPI Microservice & Transactional Supabase Allocation Engine)
# ==============================================================================

from typing import List, Dict, Any
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from supabase import Client

from app.database import get_supabase, check_db_health
from app.schemas import (
    RoomOut, 
    StudentCreate, 
    StudentOut, 
    HealthResponse, 
    DashboardStats
)
from app import crud

# Static frontend assets directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "static"

app = FastAPI(
    title="Hostel Management System API",
    description="Enterprise REST API for Hostel Operations, Room Allocation, and Student Records.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local development and Nginx reverse proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def read_root(request: Request):
    """Welcome endpoint providing service identity or serving the web dashboard for browsers."""
    accept_header = request.headers.get("accept", "")
    index_file = FRONTEND_DIR / "index.html"
    if "text/html" in accept_header and index_file.exists():
        return FileResponse(index_file)
    return {
        "service": "Hostel Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/dashboard", tags=["Frontend"], include_in_schema=False)
def serve_dashboard():
    """Direct route to access CampusStay frontend dashboard."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Frontend static assets not installed in container"}


@app.get("/styles.css", include_in_schema=False)
def serve_css():
    """Serves stylesheet for direct browser access."""
    css_file = FRONTEND_DIR / "styles.css"
    if css_file.exists():
        return FileResponse(css_file, media_type="text/css")
    raise HTTPException(status_code=404, detail="Stylesheet not found")


@app.get("/app.js", include_in_schema=False)
def serve_js():
    """Serves frontend client application script."""
    js_file = FRONTEND_DIR / "app.js"
    if js_file.exists():
        return FileResponse(js_file, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript asset not found")


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["Monitoring"]
)
def health_check(response: Response):
    """
    Pings Supabase database to verify connectivity.
    Returns HTTP 200 with status UP if connected, or HTTP 503 with status DOWN if unreachable.
    """
    is_healthy = check_db_health()
    if not is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "DOWN", "database": "DISCONNECTED"}
    return {"status": "UP", "database": "CONNECTED"}


@app.get(
    "/api/rooms",
    response_model=List[RoomOut],
    status_code=status.HTTP_200_OK,
    tags=["Rooms"]
)
def list_rooms(client: Client = Depends(get_supabase)):
    """
    Retrieve all rooms in the hostel with capacity, occupancy, and status.
    """
    try:
        return crud.get_all_rooms(client)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch rooms: {str(exc)}"
        )


@app.get(
    "/api/students",
    response_model=List[StudentOut],
    status_code=status.HTTP_200_OK,
    tags=["Students"]
)
def list_students(client: Client = Depends(get_supabase)):
    """
    Retrieve all registered students with their assigned room details joined.
    """
    try:
        return crud.get_all_students(client)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch students: {str(exc)}"
        )


@app.post(
    "/api/students",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
def create_student_allocation(
    student_payload: StudentCreate, 
    client: Client = Depends(get_supabase)
):
    """
    Validate student payload, check room capacity, allocate room transactionally,
    update room occupancy and status (marking FULL if capacity met), and record student.
    """
    return crud.allocate_student(client, student_payload)


@app.get(
    "/api/stats",
    response_model=DashboardStats,
    status_code=status.HTTP_200_OK,
    tags=["Analytics"]
)
def get_stats(client: Client = Depends(get_supabase)):
    """
    Retrieve real-time hostel KPI statistics (room counts, bed vacancy, occupancy percentage).
    """
    try:
        return crud.get_dashboard_statistics(client)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate stats: {str(exc)}"
        )
