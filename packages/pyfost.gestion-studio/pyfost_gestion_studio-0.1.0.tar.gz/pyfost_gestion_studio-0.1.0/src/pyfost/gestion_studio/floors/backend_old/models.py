from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    JSON,
    Enum as SQLEnum,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from .database import Base
import enum


# --- Enums ---
class ResourceCategoryEnum(str, enum.Enum):
    USER = "User"
    WORKSTATION = "Workstation"
    SOFTWARE_LICENSE = "SoftwareLicense"
    OTHER = "Other"


class AssignmentStatusEnum(str, enum.Enum):
    PLANNED = "Planned"
    READY = "Ready"
    ACTIVE = "Active"  # Optional: could be inferred from date
    ARCHIVED = "Archived"


class TaskStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"


# --- Models ---


class Facility(Base):
    __tablename__ = "facilities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    floors = relationship(
        "Floor", back_populates="facility", cascade="all, delete-orphan"
    )


class Floor(Base):
    __tablename__ = "floors"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)  # e.g., "Ground", "1", "Mezzanine"
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False)

    facility = relationship("Facility", back_populates="floors")
    seats = relationship("Seat", back_populates="floor", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("facility_id", "level", name="uq_facility_level"),
    )


class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, index=True)  # e.g., "A101", "B2-05"
    x_coord = Column(Float, nullable=False)
    y_coord = Column(Float, nullable=False)
    floor_id = Column(Integer, ForeignKey("floors.id"), nullable=False)

    floor = relationship("Floor", back_populates="seats")
    assignments = relationship(
        "Assignment", back_populates="seat", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("floor_id", "code", name="uq_floor_seat_code"),
        Index("ix_seat_floor_id_code", "floor_id", "code"),  # Index for lookups
    )


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    resource_category = Column(
        SQLEnum(ResourceCategoryEnum), nullable=False, index=True
    )
    identifier = Column(
        String, unique=True, index=True, nullable=False
    )  # e.g., username, asset tag, license key
    properties = Column(
        JSON, nullable=True
    )  # Store specific attributes (e.g., {"email": "...", "department": "..."})

    assignments = relationship("Assignment", back_populates="resource")


class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    status = Column(
        SQLEnum(AssignmentStatusEnum),
        nullable=False,
        default=AssignmentStatusEnum.PLANNED,
        index=True,
    )

    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    seat = relationship("Seat", back_populates="assignments")
    resource = relationship("Resource", back_populates="assignments")
    tasks = relationship(
        "Task", back_populates="assignment", cascade="all, delete-orphan"
    )

    # Index for the most critical query: finding assignments active on a date for a seat/floor
    __table_args__ = (
        Index("ix_assignment_seat_dates", "seat_id", "start_date", "end_date"),
        Index(
            "ix_assignment_resource_dates", "resource_id", "start_date", "end_date"
        ),  # Prevent resource double-booking
    )


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(
        String, nullable=False, index=True
    )  # e.g., "Setup Workstation", "Install Software X", "Clean Desk"
    status = Column(
        SQLEnum(TaskStatusEnum),
        nullable=False,
        default=TaskStatusEnum.PENDING,
        index=True,
    )
    assignee = Column(String, nullable=True, index=True)  # User ID or name
    notes = Column(String, nullable=True)

    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    assignment = relationship("Assignment", back_populates="tasks")
