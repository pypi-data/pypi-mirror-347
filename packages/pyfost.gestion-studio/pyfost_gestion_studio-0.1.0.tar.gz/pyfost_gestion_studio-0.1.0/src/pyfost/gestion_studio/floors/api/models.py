from __future__ import annotations

# This duplicates all the query and response models from the backend.
# Which sucks.
# But in real world situation, this api client would be generated from
# the backend openapi specs, and all would be duplicated.
# So I guess that's ok.
# (and we should generate this api from the backend openapi!!!)

import enum
import uuid
import datetime

from pydantic import BaseModel, Field, EmailStr, UUID4


class FloorsModel(BaseModel):
    pass


class Facility(FloorsModel):
    id: uuid.UUID | None
    name: str
    floors: list[Floor]


class Floor(FloorsModel):
    id: uuid.UUID | None
    name: str
    facility: Facility
    seats: list[Seat]


class Seat(FloorsModel):
    id: uuid.UUID | None
    code: str
    position_x: int
    position_y: int

    floor: Floor
    assignations: list[Assignation]


class ResourceCategory(str, enum.Enum):
    USER = "User"
    WORKSTATION = "Workstation"
    SOFTWARE_LICENSE = "SoftwareLicense"
    OTHER = "Other"


class Resource(FloorsModel):
    id: uuid.UUID | None
    category: ResourceCategory
    name: str
    properties: str  # JsonValue
    assignations: list[Assignation]


class AssignationStatus(str, enum.Enum):
    PLANNED = "Planned"
    WIP = "In Progress"
    READY = "Ready"


class Assignation(FloorsModel):
    id: uuid.UUID | None
    start_date: datetime.date
    end_date: datetime.date
    status: AssignationStatus
    seat: Seat
    resource: Resource
    tasks: list[Task]


class TaskType(str, enum.Enum):
    SETUP_WORKSTATION = "Setup Workstation"
    INSTALL_SOFTWARES = "Install Softwares"


class TaskStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"


class Task(FloorsModel):
    id: uuid.UUID | None
    type: TaskType
    status: TaskStatus
    notes: str
    assignation_id: uuid.UUID | None
    assignation: Assignation
