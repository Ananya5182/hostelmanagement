from datetime import date
from typing import Optional, Any
from pydantic import BaseModel, Field, EmailStr, computed_field, ConfigDict


class RoomBase(BaseModel):
    """Base schema for Room model."""
    room_number: str = Field(..., description="Unique room number (e.g. A-101)")
    block_name: Optional[str] = Field("Block A", description="Building block name")
    room_type: Optional[str] = Field("SHARED_DOUBLE", description="Room classification")
    capacity: int = Field(..., ge=1, description="Total bed capacity")
    occupied: int = Field(0, ge=0, description="Current occupied beds")
    monthly_fee: Optional[float] = Field(0.0, ge=0.0, description="Monthly rent fee")
    status: str = Field("AVAILABLE", description="Room status (AVAILABLE, FULL, MAINTENANCE)")

    model_config = ConfigDict(from_attributes=True)


class RoomCreate(RoomBase):
    """Schema for creating a new room."""
    pass


class RoomOut(RoomBase):
    """Schema for room output in API responses."""
    id: int = Field(..., description="Unique room identifier")

    @computed_field
    @property
    def occupancy(self) -> int:
        """Alias property ensuring compatibility with occupancy field requirements."""
        return self.occupied


class StudentBase(BaseModel):
    """Base schema for Student details."""
    name: str = Field(..., min_length=2, max_length=100, description="Student full name")
    email: EmailStr = Field(..., description="Student email address")
    phone: str = Field(..., min_length=7, max_length=20, description="Student primary phone number")
    emergency_contact: Optional[str] = Field(None, max_length=20, description="Emergency contact phone")
    room_id: int = Field(..., description="ID of the room to allocate")
    check_in_date: Optional[str] = Field(None, description="Check-in date (YYYY-MM-DD)")


class StudentCreate(StudentBase):
    """Schema for student room allocation request."""
    pass


class StudentOut(StudentBase):
    """Schema for student record output with joined room details."""
    id: int = Field(..., description="Unique student identifier")
    created_at: Optional[str] = Field(None, description="Registration timestamp")
    rooms: Optional[Any] = Field(None, description="Joined room details object")

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    """Schema for system health check status."""
    status: str = Field("UP", description="Overall service status")
    database: str = Field("CONNECTED", description="Database connection status")


class DashboardStats(BaseModel):
    """Schema for dashboard KPI summary statistics."""
    total_rooms: int = Field(..., description="Total number of rooms")
    total_capacity: int = Field(..., description="Sum of all bed capacities")
    total_occupied: int = Field(..., description="Total currently occupied beds")
    available_beds: int = Field(..., description="Vacant beds available for allocation")
    occupancy_rate: float = Field(..., description="Overall occupancy percentage")
