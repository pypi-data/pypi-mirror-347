import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, col
from sqlalchemy.exc import IntegrityError

from ..database import get_session
from ..models import (
    AssignationBase,
    Assignation,
    AssignationStatus,
)

router = APIRouter(
    prefix="/assignations",
    tags=["Floors Assignations"],
)
