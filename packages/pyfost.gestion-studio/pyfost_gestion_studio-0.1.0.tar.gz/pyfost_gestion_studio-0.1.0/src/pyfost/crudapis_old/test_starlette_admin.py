import uuid
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Relationship, SQLModel, select, delete
from starlette_admin.contrib.sqla import Admin, ModelView

# --- Database Setup ---
DATABASE_URL = "sqlite+aiosqlite:///./test_admin.db"
# Use connect_args for SQLite thread safety with FastAPI
connect_args = {"check_same_thread": False}
engine = create_async_engine(DATABASE_URL, echo=True, connect_args=connect_args)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# --- SQLModel Definitions (combines Pydantic + SQLAlchemy) ---
# Note: Using Int IDs for simplicity with SQLite auto-increment and relationships


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    full_name: Optional[str] = None
    active: bool = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Define the relationship to Post (one-to-many)
    posts: List["Post"] = Relationship(back_populates="author")


class UserRead(UserBase):  # Pydantic-like model for API output
    id: int


class UserCreate(UserBase):  # Pydantic-like model for API input
    pass


class PostBase(SQLModel):
    title: str = Field(index=True)
    content: str
    published: bool = False


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id")  # Required relationship
    # Define the relationship back to User (many-to-one)
    author: User = Relationship(back_populates="posts")


class PostRead(PostBase):  # API output schema
    id: int
    author_id: int


class PostCreate(PostBase):  # API input schema
    author_id: int


# --- Database Dependency ---
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


# --- Database Initialization ---
async def create_db_and_tables():
    # Use run_sync for create_all with async engine
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Uncomment to reset DB on start
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created (if they didn't exist).")
    # Optional: Seed initial data
    async with async_session_maker() as session:
        statement = select(User).where(User.username == "admin")
        results = await session.execute(statement)
        admin_user = results.scalars().first()
        if not admin_user:
            print("Seeding initial admin user...")
            user = User(
                username="admin",
                email="admin@example.com",
                full_name="Admin User",
                active=True,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)  # Get the generated ID
            print(f"Admin user created with ID: {user.id}")
            post1 = Post(
                title="First Post",
                content="Hello World!",
                published=True,
                author_id=user.id,
            )
            post2 = Post(
                title="Second Post",
                content="Another one",
                published=False,
                author_id=user.id,
            )
            session.add_all([post1, post2])
            await session.commit()
            print("Seeded initial posts.")


# --- Starlette Admin Views ---
class UserAdminView(ModelView):
    model = User
    icon = "fa fa-users"
    fields = [
        "id",
        "username",
        "email",
        "full_name",
        "active",
        "posts",  # Can display related posts (usually as links or count)
    ]
    searchable_fields = ["username", "email", "full_name"]
    sortable_fields = ["id", "username", "email", "active"]
    fields_excluded_from_create = [
        "id",
        "posts",
    ]  # Don't set posts directly on user creation
    fields_excluded_from_edit = [
        "id",
        "posts",
    ]  # Don't edit posts directly from user form


class PostAdminView(ModelView):
    model = Post
    icon = "fa fa-blog"
    fields = ["id", "title", "published", "author"]  # Show related author
    searchable_fields = ["title", "content"]
    sortable_fields = ["id", "title", "published", "author_id"]
    fields_excluded_from_create = ["id"]
    fields_excluded_from_edit = ["id"]
    # Allows selecting the author when creating/editing a Post
    fields_default_sort = [("id", True)]  # Sort by ID descending by default


# --- FastAPI Application Setup ---
app = FastAPI(
    title="FastAPI with Starlette Admin & SQLModel",
    on_startup=[create_db_and_tables],  # Create tables on startup
)

# --- API Router (Manual CRUD implementation) ---
api_router = APIRouter(prefix="/api")


@api_router.post("/users/", response_model=UserRead, status_code=201)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    # Check for existing user (example)
    statement = select(User).where(User.username == user.username)
    results = await session.execute(statement)
    db_user = results.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = User.model_validate(user)  # Convert UserCreate to User model
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@api_router.get("/users/", response_model=List[UserRead])
async def read_users(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    statement = select(User).offset(offset).limit(limit)
    results = await session.execute(statement)
    users = results.scalars().all()
    return users


@api_router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api_router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    # Check if user exists first
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Example: Handle related posts (either delete them or set author_id to null if allowed)
    # For simplicity, let's prevent deletion if posts exist
    statement = (
        select(Post).where(Post.author_id == user_id).limit(1)
    )  # Check if any posts exist
    result = await session.execute(statement)
    if result.scalars().first():
        raise HTTPException(
            status_code=400, detail="Cannot delete user with existing posts"
        )

    await session.delete(user)
    await session.commit()
    return None  # Return None for 204 No Content


# --- TODO: Add API endpoints for Posts (similar structure) ---
# @api_router.post("/posts/", ...)
# @api_router.get("/posts/", ...)
# @api_router.get("/posts/{post_id}", ...)
# @api_router.put("/posts/{post_id}", ...) # Update
# @api_router.delete("/posts/{post_id}", ...)

# Include the API router in the main app
app.include_router(api_router)

# --- Starlette Admin Setup & Mounting ---
admin = Admin(engine, title="MyApp Admin Panel")  # Use the SQLAlchemy async engine

# Add the model views to the admin instance
admin.add_view(UserAdminView(User, icon="fa fa-users"))
admin.add_view(PostAdminView(Post, icon="fa fa-blog"))

# Mount the admin interface onto the FastAPI app
admin.mount_to(app)


# --- Root endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome! API at /api, Admin UI at /admin"}


# --- Main execution (for running with uvicorn) ---
if __name__ == "__main__":
    import uvicorn

    # Note: When running with uvicorn --reload, the startup event might run multiple times.
    # The create_db_and_tables function is idempotent due to `create_all`'s check.
    uvicorn.run("main_admin:app", host="0.0.0.0", port=8002, reload=True)
