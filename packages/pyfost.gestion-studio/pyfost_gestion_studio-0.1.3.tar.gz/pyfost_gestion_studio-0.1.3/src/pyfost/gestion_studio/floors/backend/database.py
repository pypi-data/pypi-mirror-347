from typing import Generator

from sqlmodel import create_engine, SQLModel, Session, text, SQLModel, MetaData
from sqlalchemy.orm import registry

FLOORS_DATABASE_URL = "sqlite:///./fost.gestion_studio.floors.db"

floors_engine = create_engine(FLOORS_DATABASE_URL, echo=False)
floors_registry = registry()


class FloorsSQLModel(SQLModel, registry=floors_registry):
    pass


def create_db_and_tables():
    FloorsSQLModel.metadata.create_all(floors_engine)
    if floors_engine.url.drivername.lower().startswith("sqlite://"):
        with floors_engine.connect() as connection:
            connection.execute(text("PRAGMA foreign_keys=ON"))  # for SQLite only


def get_session() -> Generator[Session, None, None]:
    with Session(floors_engine) as session:
        yield session
