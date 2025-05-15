from typing import Generator

from sqlmodel import create_engine, SQLModel, Session, text, SQLModel, MetaData
from sqlalchemy.orm import registry

PYFOST_PROJECTS_DATABASE_URL = "sqlite:///./fost.gestion_studio.projects.db"
# For PostgreSQL (example, ensure you have python-dotenv and a .env file or set env var)
# from dotenv import load_dotenv
# import os
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")

# echo=True is good for development to see SQL queries
projects_engine = create_engine(PYFOST_PROJECTS_DATABASE_URL, echo=False)
projects_registry = registry()


class FloorsSQLModel(SQLModel, registry=projects_registry):
    pass


def create_db_and_tables():
    FloorsSQLModel.metadata.create_all(projects_engine)
    if projects_engine.url.drivername.lower().startswith("sqlite://"):
        with projects_engine.connect() as connection:
            connection.execute(text("PRAGMA foreign_keys=ON"))  # for SQLite only


def get_session() -> Generator[Session, None, None]:
    with Session(projects_engine) as session:
        yield session
