import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_supabase


client = TestClient(app)


# Sample mock data
MOCK_ROOMS = [
    {
        "id": 1,
        "room_number": "A-101",
        "block_name": "Block A",
        "room_type": "SHARED_DOUBLE",
        "capacity": 2,
        "occupied": 1,
        "monthly_fee": 6000.0,
        "status": "AVAILABLE"
    },
    {
        "id": 2,
        "room_number": "A-102",
        "block_name": "Block A",
        "room_type": "SHARED_DOUBLE",
        "capacity": 2,
        "occupied": 2,
        "monthly_fee": 6000.0,
        "status": "FULL"
    },
    {
        "id": 3,
        "room_number": "B-201",
        "block_name": "Block B",
        "room_type": "SINGLE_DELUXE",
        "capacity": 1,
        "occupied": 0,
        "monthly_fee": 9500.0,
        "status": "MAINTENANCE"
    }
]

MOCK_STUDENTS = [
    {
        "id": 101,
        "name": "Aarav Sharma",
        "email": "aarav.sharma@example.com",
        "phone": "+919876543210",
        "emergency_contact": "+919876543299",
        "room_id": 1,
        "check_in_date": "2026-08-01",
        "created_at": "2026-10-02T10:00:00Z",
        "rooms": MOCK_ROOMS[0]
    }
]


def test_root_endpoint():
    """Verify welcome root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Hostel Management System API"
    assert "health" in data


@patch("app.main.check_db_health", return_value=True)
def test_health_check_success(mock_health):
    """Verify /health returns HTTP 200 and CONNECTED status when database is reachable."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert data["database"] == "CONNECTED"


@patch("app.main.check_db_health", return_value=False)
def test_health_check_failure(mock_health):
    """Verify /health returns HTTP 503 and DISCONNECTED status when database is unreachable."""
    response = client.get("/health")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "DOWN"
    assert data["database"] == "DISCONNECTED"


def test_list_rooms():
    """Verify /api/rooms returns room list with occupancy and status."""
    mock_supabase = MagicMock()
    mock_query = MagicMock()
    mock_supabase.table.return_value = mock_query
    mock_query.select.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.execute.return_value = MagicMock(data=[dict(r) for r in MOCK_ROOMS])

    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    response = client.get("/api/rooms")
    assert response.status_code == 200
    rooms = response.json()
    assert len(rooms) == 3
    assert rooms[0]["room_number"] == "A-101"
    assert rooms[0]["occupancy"] == 1
    assert rooms[0]["status"] == "AVAILABLE"

    app.dependency_overrides.clear()


def test_list_students():
    """Verify /api/students returns students with joined room details."""
    mock_supabase = MagicMock()
    mock_query = MagicMock()
    mock_supabase.table.return_value = mock_query
    mock_query.select.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.execute.return_value = MagicMock(data=[dict(s) for s in MOCK_STUDENTS])

    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    response = client.get("/api/students")
    assert response.status_code == 200
    students = response.json()
    assert len(students) == 1
    assert students[0]["name"] == "Aarav Sharma"
    assert students[0]["rooms"]["room_number"] == "A-101"

    app.dependency_overrides.clear()


def test_allocate_student_success():
    """
    Verify POST /api/students validates room capacity, allocates student,
    and updates room status to FULL if capacity is reached.
    """
    mock_supabase = MagicMock()

    # Room has capacity 2, currently occupied 1 -> after allocation: occupied 2, status FULL
    target_room = dict(MOCK_ROOMS[0])
    updated_room = {**target_room, "occupied": 2, "status": "FULL"}

    created_student = {
        "id": 202,
        "name": "Priya Nair",
        "email": "priya.nair@example.com",
        "phone": "+919811223344",
        "emergency_contact": "+919811223300",
        "room_id": 1,
        "check_in_date": "2026-08-10",
        "created_at": "2026-10-02T12:00:00Z"
    }

    # Setup mock behavior for tables
    def mock_table(table_name):
        query = MagicMock()
        if table_name == "rooms":
            # select room by id
            query.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[target_room])
            # update room
            query.update.return_value.eq.return_value.execute.return_value = MagicMock(data=[updated_room])
        elif table_name == "students":
            # insert student
            query.insert.return_value.execute.return_value = MagicMock(data=[created_student])
            # select student with joined room
            full_record = {**created_student, "rooms": updated_room}
            query.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[full_record])
        return query

    mock_supabase.table.side_effect = mock_table
    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    payload = {
        "name": "Priya Nair",
        "email": "priya.nair@example.com",
        "phone": "+919811223344",
        "emergency_contact": "+919811223300",
        "room_id": 1,
        "check_in_date": "2026-08-10"
    }

    response = client.post("/api/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Priya Nair"
    assert data["rooms"]["status"] == "FULL"
    assert data["rooms"]["occupied"] == 2

    app.dependency_overrides.clear()


def test_allocate_student_room_full():
    """Verify POST /api/students rejects allocation if room is already at full capacity."""
    mock_supabase = MagicMock()

    # Room 2 is already FULL (capacity 2, occupied 2)
    full_room = dict(MOCK_ROOMS[1])

    query = MagicMock()
    mock_supabase.table.return_value = query
    query.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[full_room])

    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    payload = {
        "name": "Vikram Patel",
        "email": "vikram.patel@example.com",
        "phone": "+919800112233",
        "room_id": 2
    }

    response = client.post("/api/students", json=payload)
    assert response.status_code == 400
    assert "already FULL" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_allocate_student_room_maintenance():
    """Verify POST /api/students rejects allocation if room is under maintenance."""
    mock_supabase = MagicMock()

    maintenance_room = dict(MOCK_ROOMS[2])

    query = MagicMock()
    mock_supabase.table.return_value = query
    query.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[maintenance_room])

    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    payload = {
        "name": "Ravi Kumar",
        "email": "ravi.kumar@example.com",
        "phone": "+919800998877",
        "room_id": 3
    }

    response = client.post("/api/students", json=payload)
    assert response.status_code == 400
    assert "MAINTENANCE" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_allocate_student_room_not_found():
    """Verify POST /api/students returns 404 when target room ID does not exist."""
    mock_supabase = MagicMock()

    query = MagicMock()
    mock_supabase.table.return_value = query
    query.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])

    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    payload = {
        "name": "Meera Joshi",
        "email": "meera.joshi@example.com",
        "phone": "+919822334455",
        "room_id": 999
    }

    response = client.post("/api/students", json=payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

    app.dependency_overrides.clear()


def test_allocate_student_invalid_payload():
    """Verify POST /api/students returns 422 Unprocessable Entity for invalid email and missing fields."""
    payload = {
        "name": "J",  # too short
        "email": "not-an-email",
        # missing phone and room_id
    }

    response = client.post("/api/students", json=payload)
    assert response.status_code == 422


def test_dashboard_stats():
    """Verify GET /api/stats calculates accurate hostel capacity, occupancy, and rates."""
    mock_supabase = MagicMock()
    mock_query = MagicMock()
    mock_supabase.table.return_value = mock_query
    mock_query.select.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.execute.return_value = MagicMock(data=[dict(r) for r in MOCK_ROOMS])

    app.dependency_overrides[get_supabase] = lambda: mock_supabase

    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_rooms"] == 3
    assert stats["total_capacity"] == 5   # 2 + 2 + 1
    assert stats["total_occupied"] == 3   # 1 + 2 + 0
    assert stats["available_beds"] == 2   # 5 - 3
    assert stats["occupancy_rate"] == 60.0

    app.dependency_overrides.clear()
