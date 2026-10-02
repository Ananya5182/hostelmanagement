from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from supabase import Client

from app.schemas import StudentCreate, RoomOut, StudentOut


def get_all_rooms(client: Client) -> List[Dict[str, Any]]:
    """
    Fetch all rooms from the database ordered by room number.
    Ensures both 'occupied' and 'occupancy' keys are present.
    """
    response = client.table("rooms").select("*").order("room_number").execute()
    rooms_data = response.data or []
    for room in rooms_data:
        room["occupancy"] = room.get("occupied", 0)
    return rooms_data


def get_room_by_id(client: Client, room_id: int) -> Dict[str, Any]:
    """
    Fetch a single room by its primary key ID.
    Raises 404 if the room does not exist.
    """
    response = client.table("rooms").select("*").eq("id", room_id).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {room_id} not found."
        )
    room = response.data[0]
    room["occupancy"] = room.get("occupied", 0)
    return room


def get_all_students(client: Client) -> List[Dict[str, Any]]:
    """
    Fetch all students with joined room details ordered by creation date descending.
    """
    response = (
        client.table("students")
        .select("*, rooms(*)")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def allocate_student(client: Client, student_in: StudentCreate) -> Dict[str, Any]:
    """
    Allocates a room to a student with transactional validation:
    1. Validates room existence.
    2. Validates room status (not MAINTENANCE).
    3. Checks room capacity (occupied < capacity).
    4. Computes new occupancy and sets status to 'FULL' if capacity reached.
    5. Updates room record.
    6. Inserts student record.
    7. Provides rollback if insertion fails.
    """
    # 1. Fetch current room
    room = get_room_by_id(client, student_in.room_id)
    
    current_capacity = int(room.get("capacity", 0))
    current_occupied = int(room.get("occupied", 0))
    current_status = room.get("status", "AVAILABLE")

    # 2. Check room operational status
    if current_status == "MAINTENANCE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room {room.get('room_number')} is currently under MAINTENANCE and cannot be allocated."
        )

    # 3. Check capacity
    if current_occupied >= current_capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room {room.get('room_number')} is already FULL (Capacity: {current_capacity}, Occupied: {current_occupied})."
        )

    new_occupied = current_occupied + 1
    new_status = "FULL" if new_occupied >= current_capacity else "AVAILABLE"

    # 4. Update room occupancy and status
    try:
        room_update_res = (
            client.table("rooms")
            .update({"occupied": new_occupied, "status": new_status})
            .eq("id", student_in.room_id)
            .execute()
        )
        if not room_update_res.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update room occupancy."
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during room occupancy update: {str(exc)}"
        )

    # 5. Insert student record
    student_payload = {
        "name": student_in.name,
        "email": student_in.email,
        "phone": student_in.phone,
        "emergency_contact": student_in.emergency_contact,
        "room_id": student_in.room_id,
        "check_in_date": student_in.check_in_date,
    }

    try:
        student_insert_res = (
            client.table("students")
            .insert(student_payload)
            .execute()
        )
        if not student_insert_res.data:
            raise RuntimeError("Student insertion returned empty response.")
        
        created_student = student_insert_res.data[0]
    except Exception as exc:
        # Rollback room update in case of student insertion failure
        try:
            client.table("rooms").update({
                "occupied": current_occupied,
                "status": current_status
            }).eq("id", student_in.room_id).execute()
        except Exception:
            pass  # Log or capture rollback exception
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record student allocation; changes rolled back. Error: {str(exc)}"
        )

    # 6. Fetch complete student details joined with room
    full_student_res = (
        client.table("students")
        .select("*, rooms(*)")
        .eq("id", created_student["id"])
        .execute()
    )

    if full_student_res.data:
        return full_student_res.data[0]
    
    created_student["rooms"] = room
    return created_student


def get_dashboard_statistics(client: Client) -> Dict[str, Any]:
    """
    Computes real-time KPI metrics across all hostel rooms.
    """
    rooms = get_all_rooms(client)
    total_rooms = len(rooms)
    total_capacity = sum(r.get("capacity", 0) for r in rooms)
    total_occupied = sum(r.get("occupied", 0) for r in rooms)
    available_beds = max(0, total_capacity - total_occupied)
    occupancy_rate = round((total_occupied / total_capacity * 100), 1) if total_capacity > 0 else 0.0

    return {
        "total_rooms": total_rooms,
        "total_capacity": total_capacity,
        "total_occupied": total_occupied,
        "available_beds": available_beds,
        "occupancy_rate": occupancy_rate
    }
