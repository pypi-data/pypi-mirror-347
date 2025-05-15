import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Use environment variable or default to SQLite
# Example .env file:
# DATABASE_URL="postgresql://user:password@host:port/database"
# DATABASE_URL="mysql+mysqlclient://user:password@host:port/database"
# DATABASE_URL="sqlite:///./seat_management.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./seat_management.db")

# Adjust connect_args for SQLite when using check_same_thread
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}  # Needed only for SQLite

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create all tables (call once at startup or use Alembic)
def init_db():
    Base.metadata.create_all(bind=engine)


# Example Usage (call this from main.py on startup if not using Alembic)
# init_db()
