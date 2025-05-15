from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import date
from .models import ResourceCategoryEnum, AssignmentStatusEnum, TaskStatusEnum


# --- Base Schemas (for common fields) ---
class FacilityBase(BaseModel):
    name: str


class FloorBase(BaseModel):
    level: str


class SeatBase(BaseModel):
    code: str
    x_coord: float
    y_coord: float


class ResourceBase(BaseModel):
    resource_category: ResourceCategoryEnum
    identifier: str = Field(
        ..., description="Unique identifier (e.g., username, asset tag, license key)"
    )
    properties: Optional[Dict[str, Any]] = None


class AssignmentBase(BaseModel):
    start_date: date
    end_date: date

    @validator("end_date")
    def end_date_must_be_after_start_date(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("End date must be on or after start date")
        return v


class TaskBase(BaseModel):
    task_type: str
    assignee: Optional[str] = None
    notes: Optional[str] = None


# --- Create Schemas (for POST requests) ---
class FacilityCreate(FacilityBase):
    pass


class FloorCreate(FloorBase):
    pass  # facility_id will be path parameter


class SeatCreate(SeatBase):
    pass  # floor_id will be path parameter


class ResourceCreate(ResourceBase):
    # Add specific validation per category if needed later
    pass


class AssignmentCreate(AssignmentBase):
    seat_id: int
    resource_id: int


class TaskCreate(TaskBase):
    pass  # assignment_id will be added internally


# --- Update Schemas (for PUT/PATCH requests) ---
class TaskUpdate(BaseModel):
    status: Optional[TaskStatusEnum] = None
    assignee: Optional[str] = None
    notes: Optional[str] = None


# --- Read Schemas (for GET responses) ---
# Use ORM mode to automatically map SQLAlchemy models to Pydantic schemas
class OrmBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Pydantic V2 equivalent of orm_mode = True


class Task(OrmBaseModel, TaskBase):
    id: int
    assignment_id: int
    status: TaskStatusEnum


class Resource(OrmBaseModel, ResourceBase):
    id: int


class Assignment(OrmBaseModel, AssignmentBase):
    id: int
    status: AssignmentStatusEnum
    seat_id: int
    resource_id: int
    resource: Resource  # Nested resource details
    tasks: List[Task] = []


class Seat(OrmBaseModel, SeatBase):
    id: int
    floor_id: int
    # Optionally include assignments, but might be too much data usually
    # assignments: List[Assignment] = []


class Floor(OrmBaseModel, FloorBase):
    id: int
    facility_id: int
    seats: List[Seat] = []  # Include seats when getting floor details


class Facility(OrmBaseModel, FacilityBase):
    id: int
    floors: List[Floor] = []  # Include floors when getting facility details


# --- Specific Response Schemas ---
class SeatAssignmentDetail(OrmBaseModel):
    seat_code: str = Field(alias="seat.code")  # Example of accessing related field
    resource_identifier: str = Field(alias="resource.identifier")
    resource_category: ResourceCategoryEnum = Field(alias="resource.resource_category")
    start_date: date
    end_date: date
    assignment_status: AssignmentStatusEnum = Field(alias="status")
    assignment_id: int = Field(alias="id")


# --- Import/Export Schema ---
class ExportData(BaseModel):
    facilities: List[Facility]  # Export full nested structure
    resources: List[Resource]  # Export resources separately
    # Assignments are implicitly exported via facilities -> floors -> seats
    # Tasks are implicitly exported via assignments


class ImportData(BaseModel):
    facilities: List[FacilityCreate]  # Use Create schemas for import data structure
    floors: List[FloorCreate]  # Need association info
    seats: List[SeatCreate]  # Need association info
    resources: List[ResourceCreate]
    assignments: List[AssignmentCreate]  # Need association info
    # We need a way to link imported floors/seats/assignments back to their parents

    # --- Refined Import Schema ---
    # It's often easier to import flat lists and reconstruct relationships
    # Or provide linking keys (e.g., facility_name, floor_level, seat_code)

    # Let's try a structure that's easier to process on import


class ImportFloorData(FloorCreate):
    facility_name: str  # Link by name


class ImportSeatData(SeatCreate):
    facility_name: str
    floor_level: str  # Link by facility name + floor level


class ImportAssignmentData(AssignmentCreate):
    facility_name: str
    floor_level: str
    seat_code: str  # Link seat by code/floor/facility
    resource_identifier: str  # Link resource by identifier
    # Override base fields since we link differently
    seat_id: Optional[int] = None  # Remove these, use lookup fields
    resource_id: Optional[int] = None


class FullImportData(BaseModel):
    facilities: List[FacilityCreate]
    floors: List[ImportFloorData]
    seats: List[ImportSeatData]
    resources: List[ResourceCreate]
    assignments: List[ImportAssignmentData]  # Tasks will be auto-generated
