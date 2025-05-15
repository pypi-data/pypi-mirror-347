# main.py
import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI
import uvicorn  # Import uvicorn here

# Import the framework components
from .datastore import InMemoryDataStore
from .builder import CrudApiBuilder
from .nicegui_builder import NiceGuiBuilder  # Import the new builder


# --- 1. Define your Pydantic Models ---
class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str = Field(..., min_length=3)
    email: str
    full_name: Optional[str] = None
    active: bool = True


class Post(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(..., min_length=5)
    content: str
    published: bool = False
    author_id: uuid.UUID  # Reference to User ID - GUI will just show the UUID for now


# --- 2. Choose a DataStore ---
data_store = InMemoryDataStore()

# --- 3. Define the list of models your API will manage ---
api_models = [User, Post]

# --- 4. Create the FastAPI app ---
app = FastAPI(
    title="My Auto-Generated CRUD App",
    description="An API and GUI built using the lightweight framework",
    version="1.0.0",
)

# --- 5. Instantiate and use the CrudApiBuilder ---
api_prefix = "/v1"  # Define prefix for API
crud_builder = CrudApiBuilder(
    models=api_models,
    data_store=data_store,
    id_field="id",
    id_type=uuid.UUID,  # Ensure this matches your models
    api_prefix=api_prefix,
)
crud_builder.attach_to_app(app)  # Attach API routes

# --- 6. Instantiate and use the NiceGuiBuilder ---
# Make sure the api_base_url matches the full URL where the API will be served
# For local dev, uvicorn default is http://127.0.0.1:8000
# Important: Construct the full base URL including the api_prefix
api_base_url = f"http://127.0.0.1:8001{api_prefix}"

gui_builder = NiceGuiBuilder(
    models=api_models,
    api_base_url=api_base_url,
    id_field="id",
    page_prefix="/gui",  # Base path for GUI pages
)
# Use a proper secret in production!
gui_builder.attach_to_app(
    app, storage_secret="my_development_secret_key"
)  # Attach GUI pages


# --- 7. Optional: Add Root Redirect or Landing Page ---
@app.get("/")
async def root():
    # Redirect root to the first GUI page or a dashboard
    first_gui_path = f"{gui_builder.page_prefix}/{gui_builder._get_plural_entity_name(api_models[0])}"
    return {
        "message": "Welcome! API at /docs, GUI starts at /gui",
        "gui_link": first_gui_path,
    }


# Redirect to GUI page could also be done:
# from fastapi.responses import RedirectResponse
# @app.get("/")
# async def root_redirect():
#      first_gui_path = f"{gui_builder.page_prefix}/{gui_builder._get_plural_entity_name(api_models[0])}"
#      return RedirectResponse(url=first_gui_path)


# --- Run the application ---
# NOTE: When using ui.run_with(app), you typically don't need uvicorn.run() here
#       NiceGUI handles running the underlying FastAPI app.
#       Just run this script directly: python main.py
if __name__ == "__main__":
    print("Starting application via NiceGUI runner...")
    # Uvicorn command is not needed here when ui.run_with is used for mounting.
    # NiceGUI will start the server. Configuration (host, port) can often
    # be passed to ui.run or inferred. Let's rely on defaults for now.
    # If you need explicit control:
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    # However, ui.run_with essentially does this or similar internally.
    # Running the script directly (python main.py) should now work.
    pass  # No explicit uvicorn.run needed here.
    gui_builder.run(port=8001, reload=True)
