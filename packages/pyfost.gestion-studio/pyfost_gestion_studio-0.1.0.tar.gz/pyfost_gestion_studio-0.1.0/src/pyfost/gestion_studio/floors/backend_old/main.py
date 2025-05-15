import time
import json
import glob

from fastapi import FastAPI, Depends, HTTPException, Query, Body, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from . import crud, models, schemas, services
from .database import SessionLocal, engine, init_db, get_db  # Correct import
from .models import TaskStatusEnum  # Import Enums for query params

# Create tables if they don't exist (better to use Alembic for migrations)
# Consider calling this only once, maybe outside the app factory if needed
init_db()  # Uncomment this line if you want to auto-create tables on startup without migrations

app = FastAPI(title="Workplace Seat Management API")

# --- API Routers ---


# Facilities
@app.post(
    "/facilities/",
    response_model=schemas.Facility,
    status_code=status.HTTP_201_CREATED,
    tags=["Facilities"],
)
def create_facility(facility: schemas.FacilityCreate, db: Session = Depends(get_db)):
    db_facility = crud.get_facility_by_name(db, name=facility.name)
    if db_facility:
        raise HTTPException(
            status_code=400, detail=f"Facility '{facility.name}' already exists."
        )
    return crud.create_facility(db=db, facility=facility)


@app.get("/facilities/", response_model=List[schemas.Facility], tags=["Facilities"])
def read_facilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    facilities = crud.get_facilities(db, skip=skip, limit=limit)
    return facilities


@app.get(
    "/facilities/{facility_id}", response_model=schemas.Facility, tags=["Facilities"]
)
def read_facility(facility_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_facility = crud.get_facility(db, facility_id=facility_id)
    if db_facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    # Manually load relationships if needed and not defined in schema or default loading
    # This uses the relationships defined in models.py and schemas.py `from_attributes=True`
    return db_facility


# Floors
@app.post(
    "/facilities/{facility_id}/floors/",
    response_model=schemas.Floor,
    status_code=status.HTTP_201_CREATED,
    tags=["Floors"],
)
def create_floor_for_facility(
    facility_id: int = Path(..., gt=0),
    floor: schemas.FloorCreate = Body(...),
    db: Session = Depends(get_db),
):
    db_facility = crud.get_facility(db, facility_id=facility_id)
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    db_floor = crud.get_floor_by_level(db, facility_id=facility_id, level=floor.level)
    if db_floor:
        raise HTTPException(
            status_code=400,
            detail=f"Floor level '{floor.level}' already exists in facility '{db_facility.name}'",
        )
    return crud.create_floor(db=db, floor=floor, facility_id=facility_id)


@app.get(
    "/facilities/{facility_id}/floors/",
    response_model=List[schemas.Floor],
    tags=["Floors"],
)
def read_floors_for_facility(
    facility_id: int = Path(..., gt=0),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    db_facility = crud.get_facility(db, facility_id=facility_id)
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    floors = crud.get_floors_by_facility(
        db, facility_id=facility_id, skip=skip, limit=limit
    )
    return floors


@app.get("/floors/{floor_id}", response_model=schemas.Floor, tags=["Floors"])
def read_floor(floor_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_floor = crud.get_floor(db, floor_id=floor_id)
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return db_floor


# Seats
@app.post(
    "/floors/{floor_id}/seats/",
    response_model=schemas.Seat,
    status_code=status.HTTP_201_CREATED,
    tags=["Seats"],
)
def create_seat_for_floor(
    floor_id: int = Path(..., gt=0),
    seat: schemas.SeatCreate = Body(...),
    db: Session = Depends(get_db),
):
    db_floor = crud.get_floor(db, floor_id=floor_id)
    if not db_floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    db_seat = crud.get_seat_by_code(db, floor_id=floor_id, code=seat.code)
    if db_seat:
        raise HTTPException(
            status_code=400,
            detail=f"Seat code '{seat.code}' already exists on this floor",
        )
    return crud.create_seat(db=db, seat=seat, floor_id=floor_id)


@app.get("/floors/{floor_id}/seats/", response_model=List[schemas.Seat], tags=["Seats"])
def read_seats_for_floor(
    floor_id: int = Path(..., gt=0),
    skip: int = 0,
    limit: int = 1000,  # Allow fetching more seats per floor
    db: Session = Depends(get_db),
):
    db_floor = crud.get_floor(db, floor_id=floor_id)
    if not db_floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    seats = crud.get_seats_by_floor(db, floor_id=floor_id, skip=skip, limit=limit)
    return seats


@app.get("/seats/{seat_id}", response_model=schemas.Seat, tags=["Seats"])
def read_seat(seat_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_seat = crud.get_seat(db, seat_id=seat_id)
    if db_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return db_seat


# Resources
@app.post(
    "/resources/",
    response_model=schemas.Resource,
    status_code=status.HTTP_201_CREATED,
    tags=["Resources"],
)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    db_resource = crud.get_resource_by_identifier(db, identifier=resource.identifier)
    if db_resource:
        raise HTTPException(
            status_code=400,
            detail=f"Resource with identifier '{resource.identifier}' already exists",
        )
    # Add validation for properties based on resource_category if needed
    # e.g., if resource.resource_category == models.ResourceCategoryEnum.USER: ... check for email property
    return crud.create_resource(db=db, resource=resource)


@app.get("/resources/", response_model=List[schemas.Resource], tags=["Resources"])
def read_resources(
    category: Optional[models.ResourceCategoryEnum] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    resources = crud.get_resources(db, category=category, skip=skip, limit=limit)
    return resources


@app.get(
    "/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"]
)
def read_resource(resource_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource


# Assignments
@app.post(
    "/assignments/",
    response_model=schemas.Assignment,
    status_code=status.HTTP_201_CREATED,
    tags=["Assignments"],
)
def create_assignment(
    assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)
):
    """Creates an assignment and associated 'Planned' tasks."""
    try:
        # Use the service function to handle creation and task generation
        db_assignment = services.create_assignment_with_tasks(
            db=db, assignment=assignment
        )
        return db_assignment
    except ValueError as e:  # Catch validation errors from the service
        raise HTTPException(
            status_code=404, detail=str(e)
        )  # 404 if seat/resource not found
    except Exception as e:  # Catch potential DB or other errors
        # Log the exception e
        print(f"Error creating assignment: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error during assignment creation."
        )


@app.get(
    "/assignments/{assignment_id}",
    response_model=schemas.Assignment,
    tags=["Assignments"],
)
def read_assignment(
    assignment_id: int = Path(..., gt=0), db: Session = Depends(get_db)
):
    db_assignment = crud.get_assignment(db, assignment_id=assignment_id)
    if db_assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment


# --- Core Requirement: List Assignments for a Floor at a Date ---
@app.get(
    "/floors/{floor_id}/assignments/",
    response_model=List[schemas.SeatAssignmentDetail],
    tags=["Assignments", "Query"],
)
def read_assignments_for_floor_on_date(
    floor_id: int = Path(..., gt=0),
    date: date = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    """Lists resources assigned to all seats of a floor at a given date."""
    db_floor = crud.get_floor(db, floor_id=floor_id)
    if not db_floor:
        raise HTTPException(status_code=404, detail="Floor not found")

    assignments = crud.get_assignments_for_floor_at_date(
        db=db, floor_id=floor_id, target_date=date
    )

    # Convert results to the specific response schema
    results = []
    for assgn in assignments:
        # Manually create the SeatAssignmentDetail if automatic mapping isn't perfect
        # Pydantic v2's from_attributes handles nested relationships better
        detail = schemas.SeatAssignmentDetail(
            seat_code=assgn.seat.code,  # Access related object attributes
            resource_identifier=assgn.resource.identifier,
            resource_category=assgn.resource.resource_category,
            start_date=assgn.start_date,
            end_date=assgn.end_date,
            assignment_status=assgn.status,
            assignment_id=assgn.id,
        )
        results.append(detail)
    return results


# Tasks
@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tasks"])
def read_tasks(
    status: Optional[TaskStatusEnum] = Query(None, description="Filter by task status"),
    task_type: Optional[str] = Query(
        None, description="Filter by task type (exact match)"
    ),
    assignee: Optional[str] = Query(
        None, description="Filter by assignee (exact match)"
    ),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Lists tasks with optional filters for status, type, and assignee."""
    tasks = crud.get_tasks(
        db,
        status=status,
        task_type=task_type,
        assignee=assignee,
        skip=skip,
        limit=limit,
    )
    return tasks


@app.patch("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def update_task(
    task_id: int = Path(..., gt=0),
    task_update: schemas.TaskUpdate = Body(...),
    db: Session = Depends(get_db),
):
    """Updates a task's status, assignee, or notes."""
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = crud.update_task(db=db, task_id=task_id, task_update=task_update)

    # Check if this task completion triggers assignment status update
    if task_update.status == TaskStatusEnum.COMPLETED:
        services.check_and_update_assignment_status(
            db=db, assignment_id=updated_task.assignment_id
        )
        # Refresh task data in case status was changed by the service (though unlikely here)
        db.refresh(updated_task)

    return updated_task


@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def read_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# --- Data Import/Export ---
EXPORT_FILENAME_TEMPLATE = "data_backup-{suffix}.json"


@app.get("/data/export", tags=["Data Management"])
def export_data(db: Session = Depends(get_db)):
    """Exports all data to a JSON format."""
    try:
        all_data = crud.get_all_data(db)
        # Convert Pydantic model to JSON-serializable dict
        # Use model_dump for Pydantic V2
        data_dict = all_data.model_dump(
            mode="json"
        )  # 'json' mode ensures types like date are strings

        # Option 1: Return as JSON response (good for direct API use)
        # return data_dict

        # Option 2: Save to a file server-side (as requested for backup file)
        # Be careful with file paths in real applications
        export_filename = EXPORT_FILENAME_TEMPLATE.format(suffix=time.time())
        with open(export_filename, "w") as f:
            json.dump(data_dict, f, indent=4)
        return {"message": f"Data exported successfully to {export_filename}"}

    except Exception as e:
        print(f"Export failed: {e}")  # Log error
        raise HTTPException(status_code=500, detail=f"Data export failed: {e}")


@app.post("/data/import", tags=["Data Management"])
def import_data(
    data: schemas.FullImportData = Body(
        ...
    ),  # Use the flat structure for easier import
    db: Session = Depends(get_db),
):
    """
    Imports data from a JSON body, replacing all existing data.
    WARNING: This deletes all current data before importing.
    """
    try:
        crud.import_all_data(db, data)
        return {
            "message": "Data imported successfully. All previous data has been replaced."
        }
    except Exception as e:
        db.rollback()  # Rollback transaction on error
        print(f"Import failed: {e}")  # Log error
        raise HTTPException(status_code=500, detail=f"Data import failed: {e}")


# Optional: Endpoint to trigger import from the predefined file
@app.post("/data/import-from-file", tags=["Data Management"])
def import_data_from_file(db: Session = Depends(get_db)):
    """
    Imports data from the predefined JSON backup file, replacing all existing data.
    WARNING: This deletes all current data before importing.
    """
    import_filenames_pattern = EXPORT_FILENAME_TEMPLATE.format(suffix="*")
    filenames = glob.glob(import_filenames_pattern)
    import_filename = sorted(filenames)[-1]
    try:
        with open(import_filename, "r") as f:
            data_dict = json.load(f)
        # Validate data using Pydantic before passing to crud
        import_data_validated = schemas.FullImportData(**data_dict)
        crud.import_all_data(db, import_data_validated)
        return {
            "message": f"Data imported successfully from {import_filename!r}. All previous data has been replaced."
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Backup file '{import_filename!r}' not found."
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail=f"Invalid JSON format in {import_filename!r}."
        )
    except Exception as e:  # Includes Pydantic validation errors
        db.rollback()  # Rollback transaction on error
        print(f"Import from file {import_filename!r} failed: {e}")  # Log error
        raise HTTPException(
            status_code=500,
            detail=f"Data import from file {import_filename!r} failed: {e}",
        )


# Add a simple root endpoint
@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to the Workplace Seat Management API"}
