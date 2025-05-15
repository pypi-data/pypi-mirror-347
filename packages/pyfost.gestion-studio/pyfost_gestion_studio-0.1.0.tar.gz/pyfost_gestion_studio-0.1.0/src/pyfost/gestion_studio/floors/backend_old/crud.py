from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from . import models, schemas
from datetime import date


# --- Facility CRUD ---
def get_facility(db: Session, facility_id: int):
    return db.query(models.Facility).filter(models.Facility.id == facility_id).first()


def get_facility_by_name(db: Session, name: str):
    return db.query(models.Facility).filter(models.Facility.name == name).first()


def get_facilities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Facility).offset(skip).limit(limit).all()


def create_facility(db: Session, facility: schemas.FacilityCreate):
    db_facility = models.Facility(name=facility.name)
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility


# --- Floor CRUD ---
def get_floor(db: Session, floor_id: int):
    return db.query(models.Floor).filter(models.Floor.id == floor_id).first()


def get_floors_by_facility(
    db: Session, facility_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Floor)
        .filter(models.Floor.facility_id == facility_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_floor_by_level(db: Session, facility_id: int, level: str):
    return (
        db.query(models.Floor)
        .filter(models.Floor.facility_id == facility_id, models.Floor.level == level)
        .first()
    )


def create_floor(db: Session, floor: schemas.FloorCreate, facility_id: int):
    db_floor = models.Floor(**floor.model_dump(), facility_id=facility_id)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor


# --- Seat CRUD ---
def get_seat(db: Session, seat_id: int):
    return db.query(models.Seat).filter(models.Seat.id == seat_id).first()


def get_seats_by_floor(db: Session, floor_id: int, skip: int = 0, limit: int = 1000):
    return (
        db.query(models.Seat)
        .filter(models.Seat.floor_id == floor_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_seat_by_code(db: Session, floor_id: int, code: str):
    return (
        db.query(models.Seat)
        .filter(models.Seat.floor_id == floor_id, models.Seat.code == code)
        .first()
    )


def create_seat(db: Session, seat: schemas.SeatCreate, floor_id: int):
    db_seat = models.Seat(**seat.model_dump(), floor_id=floor_id)
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat


# --- Resource CRUD ---
def get_resource(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()


def get_resource_by_identifier(db: Session, identifier: str):
    return (
        db.query(models.Resource)
        .filter(models.Resource.identifier == identifier)
        .first()
    )


def get_resources(
    db: Session,
    category: models.ResourceCategoryEnum | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Resource)
    if category:
        query = query.filter(models.Resource.resource_category == category)
    return query.offset(skip).limit(limit).all()


def create_resource(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


# --- Assignment CRUD ---
def get_assignment(db: Session, assignment_id: int):
    return (
        db.query(models.Assignment)
        .options(
            joinedload(models.Assignment.resource),  # Eager load resource
            joinedload(models.Assignment.tasks),  # Eager load tasks
        )
        .filter(models.Assignment.id == assignment_id)
        .first()
    )


def get_assignments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Assignment).offset(skip).limit(limit).all()


# *** Crucial Query Optimization ***
def get_assignments_for_floor_at_date(
    db: Session, floor_id: int, target_date: date
) -> list[models.Assignment]:
    """
    Efficiently retrieves assignments active on a specific date for all seats on a given floor.
    Uses the indexes defined in the model.
    """
    return (
        db.query(models.Assignment)
        .join(models.Seat)
        .options(
            joinedload(models.Assignment.resource),  # Eager load resource details
            joinedload(
                models.Assignment.seat
            ),  # Eager load seat details (optional here)
        )
        .filter(
            models.Seat.floor_id == floor_id,
            models.Assignment.start_date <= target_date,
            models.Assignment.end_date >= target_date,
        )
        .all()
    )


def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    """Creates the assignment record ONLY. Task creation is handled in services."""
    db_assignment = models.Assignment(
        seat_id=assignment.seat_id,
        resource_id=assignment.resource_id,
        start_date=assignment.start_date,
        end_date=assignment.end_date,
        status=models.AssignmentStatusEnum.PLANNED,  # Always starts as Planned
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


# --- Task CRUD ---
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session,
    status: models.TaskStatusEnum | None = None,
    task_type: str | None = None,
    assignee: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if task_type:
        query = query.filter(models.Task.task_type == task_type)
    if assignee:
        query = query.filter(models.Task.assignee == assignee)
    return query.order_by(models.Task.id).offset(skip).limit(limit).all()


def create_task_for_assignment(
    db: Session, task: schemas.TaskCreate, assignment_id: int
):
    db_task = models.Task(
        **task.model_dump(),
        assignment_id=assignment_id,
        status=models.TaskStatusEnum.PENDING,  # Always start Pending
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)  # Get only provided fields
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# --- Data Management ---


def clear_all_data(db: Session):
    """WARNING: Deletes all data from tables in a specific order due to FKs"""
    # Order matters to avoid foreign key constraint errors
    db.query(models.Task).delete(synchronize_session=False)
    db.query(models.Assignment).delete(synchronize_session=False)
    db.query(models.Resource).delete(synchronize_session=False)
    db.query(models.Seat).delete(synchronize_session=False)
    db.query(models.Floor).delete(synchronize_session=False)
    db.query(models.Facility).delete(synchronize_session=False)
    db.commit()


def get_all_data(db: Session):
    """Retrieves all data for export"""
    facilities = (
        db.query(models.Facility)
        .options(
            joinedload(models.Facility.floors).joinedload(models.Floor.seats)
            # Assignments and Tasks are loaded via Assignment queries if needed,
            # but exporting them nested under seats can be massive.
            # Exporting resources separately is better.
        )
        .all()
    )
    resources = db.query(models.Resource).all()
    # Assignments and Tasks could be fetched separately if needed for the export structure
    # assignments = db.query(models.Assignment).options(joinedload(models.Assignment.tasks)).all()

    # Convert to Pydantic schemas for consistent output
    facilities_schema = [schemas.Facility.model_validate(f) for f in facilities]
    resources_schema = [schemas.Resource.model_validate(r) for r in resources]

    return schemas.ExportData(facilities=facilities_schema, resources=resources_schema)


def import_all_data(db: Session, data: schemas.FullImportData):
    """Clears existing data and imports from the provided structure"""
    clear_all_data(db)  # Clear existing data first

    # Use dictionaries to map imported names/codes to created DB IDs
    facility_map = {}  # name -> id
    floor_map = {}  # (facility_name, level) -> id
    seat_map = {}  # (facility_name, level, code) -> id
    resource_map = {}  # identifier -> id

    # 1. Import Facilities
    for facility_data in data.facilities:
        db_facility = create_facility(db, facility_data)
        facility_map[db_facility.name] = db_facility.id

    # 2. Import Floors
    for floor_data in data.floors:
        facility_id = facility_map.get(floor_data.facility_name)
        if facility_id:
            db_floor = create_floor(
                db, schemas.FloorCreate(level=floor_data.level), facility_id
            )
            floor_map[(floor_data.facility_name, db_floor.level)] = db_floor.id
        else:
            print(
                f"Warning: Facility '{floor_data.facility_name}' not found for floor '{floor_data.level}'. Skipping."
            )  # Add proper logging

    # 3. Import Seats
    for seat_data in data.seats:
        floor_id = floor_map.get((seat_data.facility_name, seat_data.floor_level))
        if floor_id:
            db_seat = create_seat(
                db,
                schemas.SeatCreate(
                    **seat_data.model_dump(exclude={"facility_name", "floor_level"})
                ),
                floor_id,
            )
            seat_map[(seat_data.facility_name, seat_data.floor_level, db_seat.code)] = (
                db_seat.id
            )
        else:
            print(
                f"Warning: Floor '{seat_data.floor_level}' in facility '{seat_data.facility_name}' not found for seat '{seat_data.code}'. Skipping."
            )

    # 4. Import Resources
    for resource_data in data.resources:
        # Handle potential duplicate identifiers if necessary (e.g., skip or update)
        existing = get_resource_by_identifier(db, resource_data.identifier)
        if not existing:
            db_resource = create_resource(db, resource_data)
            resource_map[db_resource.identifier] = db_resource.id
        else:
            resource_map[resource_data.identifier] = existing.id
            print(
                f"Warning: Resource with identifier '{resource_data.identifier}' already exists. Using existing ID."
            )

    # 5. Import Assignments (and auto-generate tasks)
    # Import using the service layer function to handle task generation
    from . import services  # Avoid circular import at top level

    for assignment_data in data.assignments:
        seat_id = seat_map.get(
            (
                assignment_data.facility_name,
                assignment_data.floor_level,
                assignment_data.seat_code,
            )
        )
        resource_id = resource_map.get(assignment_data.resource_identifier)

        if seat_id and resource_id:
            create_assign_schema = schemas.AssignmentCreate(
                seat_id=seat_id,
                resource_id=resource_id,
                start_date=assignment_data.start_date,
                end_date=assignment_data.end_date,
            )
            # Use the service to create assignment and associated tasks
            try:
                services.create_assignment_with_tasks(db, create_assign_schema)
            except ValueError as e:
                print(
                    f"Error creating assignment for seat '{assignment_data.seat_code}' / resource '{assignment_data.resource_identifier}': {e}"
                )
            # Note: Status is implicitly 'Planned'. Tasks are auto-created.
            # If the import data should specify status or tasks, the import logic needs adjustment.
        else:
            missing = []
            if not seat_id:
                missing.append(
                    f"Seat ({assignment_data.facility_name}/{assignment_data.floor_level}/{assignment_data.seat_code})"
                )
            if not resource_id:
                missing.append(f"Resource ({assignment_data.resource_identifier})")
            print(
                f"Warning: Could not find {' or '.join(missing)} for an assignment. Skipping."
            )

    # No explicit task import needed as they are generated by create_assignment_with_tasks
    # If tasks need specific statuses/assignees on import, the schema and logic must be extended.
