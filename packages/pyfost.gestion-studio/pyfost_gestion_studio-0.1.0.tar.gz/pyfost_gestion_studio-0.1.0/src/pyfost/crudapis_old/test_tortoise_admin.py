# main_tortoise.py
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise import Tortoise

# Import API and Admin generators
from tortoise_api.routers import add_routers as add_tortoise_api_routers
from femto_admin.contrib.tortoise import Admin as FemtoAdmin

# Import models (make sure models.py is in the same directory or adjust path)
from .t_models import User, Post

# --- Load Environment Variables ---
load_dotenv()

# --- Tortoise ORM Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://./db_tortoise_fallback.sqlite3")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {  # 'models' is the app name, can be anything
            "models": ["models", "aerich.models"],  # Module paths to find models
            # "models" refers to models.py
            # "aerich.models" is needed for Aerich migrations (optional but recommended)
            "default_connection": "default",
        },
    },
}


# --- Tortoise ORM Lifespan Management ---
async def init_orm():
    """Initialize Tortoise ORM and generate schemas."""
    print("Initializing Tortoise ORM...")
    await Tortoise.init(config=TORTOISE_ORM)
    print(f"Connected to DB: {DATABASE_URL}")
    print("Generating database schemas (if needed)...")
    # Creates tables if they don't exist
    await Tortoise.generate_schemas()
    print("Schema generation complete.")
    # Optional: Seed data
    user_exists = await User.exists(username="admin")
    if not user_exists:
        print("Seeding initial admin user...")
        user = await User.create(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            active=True,
        )
        await Post.create(
            title="First Post",
            content="Content for the first post.",
            published=True,
            author=user,
        )
        await Post.create(
            title="Second Post",
            content="More content here.",
            published=False,
            author=user,
        )
        print("Seeding complete.")


async def close_orm():
    """Close Tortoise ORM connections."""
    print("Closing Tortoise ORM connections...")
    await Tortoise.close_connections()
    print("Connections closed.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_orm()
    yield
    # Shutdown
    await close_orm()


# --- FastAPI Application Setup ---
app = FastAPI(
    title="Tortoise-API & Femto-Admin Demo",
    description="Automatic API and Admin UI from Tortoise ORM models",
    version="1.0.0",
    lifespan=lifespan,  # Use the lifespan context manager
)

# --- Tortoise-API Setup ---
# This function automatically discovers registered Tortoise models
# and creates FastAPI routers for them (e.g., /users, /posts)
add_tortoise_api_routers(app)
print("Tortoise-API routers added automatically.")


# --- Femto-Admin Setup ---
# Instantiate Femto Admin for Tortoise
admin = FemtoAdmin(
    # login_logo_url="https://example.com/logo.png", # Optional branding
    # logo_url="https://example.com/logo_small.png",
    # default_actions_enabled=True, # CRUD actions
    # custom_css_url=...
    # theme = "cerulean" # Example theme
)

# Register models with Femto Admin
admin.register_model(User)
admin.register_model(Post)
print("Models registered with Femto-Admin.")

# Mount the admin interface onto the FastAPI app (default path is /admin)
admin.mount_to(app)
print("Femto-Admin UI mounted at /admin.")


# --- Root Endpoint ---
@app.get("/")
async def root():
    return {
        "message": "Welcome!",
        "api_docs": "/docs",  # FastAPI Swagger UI
        "api_redoc": "/redoc",  # FastAPI ReDoc
        "admin_ui": "/admin",  # Femto-Admin UI
    }


# --- Main execution (for running with uvicorn) ---
if __name__ == "__main__":
    import uvicorn

    print("Starting Uvicorn server...")
    uvicorn.run("main_tortoise:app", host="0.0.0.0", port=8000, reload=True)
