from sqlalchemy.orm import Session
from . import crud, models, schemas
from .task_definitions import get_tasks_for_resource_type


def create_assignment_with_tasks(
    db: Session, assignment: schemas.AssignmentCreate
) -> models.Assignment:
    """
    Creates an assignment and generates its initial tasks based on resource type.
    """
    # 1. Validate Resource and Seat exist (optional, crud can handle FK constraint)
    resource = crud.get_resource(db, assignment.resource_id)
    if not resource:
        raise ValueError(f"Resource with id {assignment.resource_id} not found.")
    seat = crud.get_seat(db, assignment.seat_id)
    if not seat:
        raise ValueError(f"Seat with id {assignment.seat_id} not found.")

    # Add overlap validation here if needed (prevent assigning same seat/resource concurrently)
    # This is complex logic, potentially involving checking existing assignments

    # 2. Create the Assignment
    db_assignment = crud.create_assignment(db=db, assignment=assignment)

    # 3. Determine and Create Tasks
    task_types = get_tasks_for_resource_type(resource.resource_category)
    for task_type in task_types:
        task_create = schemas.TaskCreate(task_type=task_type)
        crud.create_task_for_assignment(
            db=db, task=task_create, assignment_id=db_assignment.id
        )

    db.refresh(db_assignment)  # Refresh to load relationship
    return db_assignment


def check_and_update_assignment_status(db: Session, assignment_id: int):
    """
    Checks if all tasks for an assignment are completed. If so, updates
    the assignment status to 'Ready'.
    """
    assignment = crud.get_assignment(db, assignment_id)
    if not assignment or assignment.status != models.AssignmentStatusEnum.PLANNED:
        return  # Only update if currently planned

    all_tasks_completed = True
    if not assignment.tasks:  # Handle case with no tasks defined
        all_tasks_completed = (
            True  # Or maybe requires manual Ready? Let's assume Ready.
        )
    else:
        for task in assignment.tasks:
            if task.status != models.TaskStatusEnum.COMPLETED:
                all_tasks_completed = False
                break

    if all_tasks_completed:
        assignment.status = models.AssignmentStatusEnum.READY
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
