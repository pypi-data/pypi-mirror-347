#!!! YOU CAN USE THIS WITH SQLModels: from __future__ import annotations

import uuid
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr

# TYPE_CHECKING block in models.py is primarily for forward references
# between SQLModel table classes themselves, if needed.
# Pydantic schema forward references are now handled within routers/schemas.py.
if TYPE_CHECKING:
    # These are SQLModel classes, not Pydantic schemas
    # pass # Usually not strictly needed if using string names in Relationship
    # For example, if User had a direct reference to Project SQLModel class
    # and vice-versa, this block would be crucial.
    # With the link table, direct User <-> Project SQLModel class refs are gone.
    # Task.assignee: Optional["User"] works because "User" is defined later in the file
    # or Python resolves it.
    pass


# --- Link Table: ProjectUsers ---
class ProjectUsers(SQLModel, table=True):
    __tablename__ = "project_users"

    project_id: uuid.UUID | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    user_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", primary_key=True
    )

    # project: Optional[Project] = Relationship(back_populates="user_links")
    # user: Optional[User] = Relationship(back_populates="project_links")


# --- Task Status Enum ---
class TaskStatus(str, Enum):
    NYS = "NYS"
    WIP = "WIP"
    DONE = "Done"


# --- User Model ---


class UserBase(SQLModel):
    login: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )

    projects: list["Project"] = Relationship(
        back_populates="users", link_model=ProjectUsers
    )
    assigned_tasks: list["Task"] = Relationship(back_populates="assignee")


# --- Project Model ---
class ProjectBase(SQLModel):
    code: str = Field(unique=True, index=True)
    title: str


class Project(ProjectBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )

    users: list["User"] = Relationship(
        back_populates="projects", link_model=ProjectUsers
    )
    tasks: List["Task"] = Relationship(back_populates="project", cascade_delete=True)


# --- Task Model ---
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.NYS)

    assignee_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", index=True, nullable=True
    )
    project_id: uuid.UUID = Field(foreign_key="project.id", index=True)


class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )

    assignee: Optional[User] = Relationship(back_populates="assigned_tasks")
    project: Project = Relationship(back_populates="tasks")
