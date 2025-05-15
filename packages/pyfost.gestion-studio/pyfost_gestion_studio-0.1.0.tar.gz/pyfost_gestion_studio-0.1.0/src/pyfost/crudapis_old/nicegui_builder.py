# framework/nicegui_builder.py
import httpx
import uuid
from typing import List, Type, Dict, Any, Optional, TypeVar
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from nicegui import ui, app as nicegui_app  # Import app for storage secret

# Import framework components and helpers
from .ui_components import entity_table, entity_form, show_confirmation_dialog

# Use a generic type variable consistent with CrudApiBuilder if needed, but less critical here
BuilderIdType = TypeVar("BuilderIdType")


# --- Simple Async API Client ---
class ApiClient:
    """Basic async client to interact with the CRUD API."""

    def __init__(self, base_url: str):
        # Ensure base_url doesn't end with / and prefix starts with /
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url)
        print(f"API Client initialized for base URL: {self.base_url}")

    def _get_path(self, entity_plural: str, item_id: Optional[Any] = None) -> str:
        path = f"/{entity_plural.lower()}"
        if item_id is not None:
            path += f"/{item_id}"
        return path

    async def get_all(self, entity_plural: str) -> List[Dict[str, Any]]:
        path = self._get_path(entity_plural)
        try:
            response = await self.client.get(path)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except httpx.HTTPStatusError as e:
            print(
                f"Error fetching all {entity_plural}: {e.response.status_code} - {e.response.text}"
            )
            ui.notify(
                f"Failed to load {entity_plural}: {e.response.status_code}",
                type="negative",
            )
            return []
        except Exception as e:
            print(f"Unexpected error fetching all {entity_plural}: {e}")
            ui.notify(
                f"An error occurred while loading {entity_plural}.", type="negative"
            )
            return []

    async def get_one(
        self, entity_plural: str, item_id: Any
    ) -> Optional[Dict[str, Any]]:
        path = self._get_path(entity_plural, item_id)
        try:
            response = await self.client.get(path)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                ui.notify(
                    f"{entity_plural.capitalize()} with ID {item_id} not found.",
                    type="warning",
                )
            else:
                print(
                    f"Error fetching {entity_plural} {item_id}: {e.response.status_code} - {e.response.text}"
                )
                ui.notify(
                    f"Failed to load item {item_id}: {e.response.status_code}",
                    type="negative",
                )
            return None
        except Exception as e:
            print(f"Unexpected error fetching {entity_plural} {item_id}: {e}")
            ui.notify(
                f"An error occurred while loading item {item_id}.", type="negative"
            )
            return None

    async def create(
        self, entity_plural: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        path = self._get_path(entity_plural)
        print("---->", path)
        try:
            response = await self.client.post(path, json=data)
            response.raise_for_status()
            ui.notify(
                f"{entity_plural.capitalize()} created successfully.", type="positive"
            )
            return response.json()
        except httpx.HTTPStatusError as e:
            print(
                f"Error creating {entity_plural}: {e.response.status_code} "  # - {e.response.text}"
            )
            # ui.notify(
            #     f"Failed to create {entity_plural}: {e.response.json().get('detail', e.response.text)}",
            #     type="negative",
            # )
            return None
        except Exception as e:
            print(f"Unexpected error creating {entity_plural}: {e}")
            ui.notify(
                f"An error occurred while creating {entity_plural}.", type="negative"
            )
            return None

    async def update(
        self, entity_plural: str, item_id: Any, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        path = self._get_path(entity_plural, item_id)
        try:
            # Remove None values unless specifically allowed by API/model? Generally good practice for PUT/PATCH.
            payload = {k: v for k, v in data.items() if v is not None}
            response = await self.client.put(path, json=payload)
            response.raise_for_status()
            ui.notify(
                f"{entity_plural.capitalize()} {item_id} updated successfully.",
                type="positive",
            )
            return response.json()
        except httpx.HTTPStatusError as e:
            print(
                f"Error updating {entity_plural} {item_id}: {e.response.status_code} - {e.response.text}"
            )
            ui.notify(
                f"Failed to update {item_id}: {e.response.json().get('detail', e.response.text)}",
                type="negative",
            )
            return None
        except Exception as e:
            print(f"Unexpected error updating {entity_plural} {item_id}: {e}")
            ui.notify(f"An error occurred while updating {item_id}.", type="negative")
            return None

    async def delete(self, entity_plural: str, item_id: Any) -> bool:
        path = self._get_path(entity_plural, item_id)
        try:
            response = await self.client.delete(path)
            response.raise_for_status()
            ui.notify(
                f"{entity_plural.capitalize()} {item_id} deleted successfully.",
                type="positive",
            )
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                ui.notify(f"Item {item_id} not found for deletion.", type="warning")
            else:
                print(
                    f"Error deleting {entity_plural} {item_id}: {e.response.status_code} - {e.response.text}"
                )
                ui.notify(
                    f"Failed to delete {item_id}: {e.response.status_code}",
                    type="negative",
                )
            return False
        except Exception as e:
            print(f"Unexpected error deleting {entity_plural} {item_id}: {e}")
            ui.notify(f"An error occurred while deleting {item_id}.", type="negative")
            return False

    async def close(self):
        await self.client.aclose()


class NiceGuiBuilder:
    """Generates NiceGUI pages for CRUD operations based on Pydantic models."""

    def __init__(
        self,
        models: List[Type[BaseModel]],
        api_base_url: str,  # e.g., "http://localhost:8000/v1"
        id_field: str = "id",
        page_prefix: str = "/gui",  # Where the GUI pages will live
    ):
        self.models = models
        self.api_client = ApiClient(base_url=api_base_url)
        self.id_field = id_field
        self.page_prefix = page_prefix.rstrip("/")
        self._generate_pages()

    def _get_entity_name(self, model: Type[BaseModel]) -> str:
        return model.__name__.lower()

    def _get_plural_entity_name(self, model: Type[BaseModel]) -> str:
        # Simple pluralization, enhance if needed
        return f"{self._get_entity_name(model)}s"

    def _generate_ui_columns(self, model: Type[BaseModel]) -> List[Dict]:
        """Generate column definitions for ui.table from Pydantic model."""
        columns = []
        schema = model.model_json_schema()
        properties = schema.get("properties", {})

        for name, props in properties.items():
            # Basic heuristic for sorting/alignment - can be refined
            field_type = props.get("type")
            align = "right" if field_type in ["integer", "number"] else "left"
            sortable = True  # Allow sorting on most fields by default

            columns.append(
                {
                    "name": name,
                    "label": props.get("title", name).replace("_", " ").title(),
                    "field": name,  # Crucial for linking data
                    "required": name in schema.get("required", []),
                    "align": align,
                    "sortable": sortable,
                }
            )
        return columns

    def _generate_pages(self):
        """Creates the NiceGUI @ui.page routes for each model."""
        print("Generating NiceGUI pages...")

        # Navigation links can be built dynamically
        nav_links = {}
        for model in self.models:
            entity_name = self._get_entity_name(model)
            plural_name = self._get_plural_entity_name(model)
            page_path = f"{self.page_prefix}/{plural_name}"
            nav_links[entity_name.capitalize()] = page_path

        for model in self.models:
            entity_name = self._get_entity_name(model)
            plural_name = self._get_plural_entity_name(model)
            page_path = f"{self.page_prefix}/{plural_name}"
            page_title = f"{model.__name__} Management"

            # Define the page creation within a function scope to capture model correctly
            def create_page(
                current_model: Type[BaseModel],
                current_plural_name: str,
                current_page_title: str,
            ):

                @ui.page(page_path, title=current_page_title)
                async def page():
                    # --- Page State ---
                    items = []  # List to hold fetched data
                    table_ref = None  # Reference to the ui.table for refresh

                    # --- API Interaction Handlers ---
                    async def load_data():
                        nonlocal items
                        fetched_items = await self.api_client.get_all(
                            current_plural_name
                        )
                        items[:] = fetched_items  # Update list in place for reactivity
                        if table_ref:
                            table_ref.update_rows(items)  # Explicitly update table rows
                        print(f"Loaded {len(items)} items for {current_plural_name}")

                    async def handle_save_create(data: Dict[str, Any]):
                        # Basic client-side validation (Pydantic handles on backend)
                        try:
                            # Attempt to parse to catch simple type errors early
                            _ = current_model(**data)
                        except ValidationError as e:
                            ui.notify(
                                f"Validation Error: {e}",
                                type="negative",
                                multi_line=True,
                            )
                            return  # Stop processing

                        new_item = await self.api_client.create(
                            current_plural_name, data
                        )
                        if new_item:
                            await load_data()  # Refresh table
                            create_dialog.close()

                    async def handle_save_edit(item_id: Any, data: Dict[str, Any]):
                        updated_item = await self.api_client.update(
                            current_plural_name, item_id, data
                        )
                        if updated_item:
                            await load_data()  # Refresh table
                            edit_dialog.close()

                    async def handle_delete(item_id: Any):
                        item = next(
                            (item for item in items if item[self.id_field] == item_id),
                            None,
                        )
                        item_repr = (
                            f"{current_model.__name__} (ID: {item_id})"
                            if not item
                            else f"{item.get('name', item.get('title', item_id))}"
                        )  # Try to get a descriptive name

                        confirmed = await show_confirmation_dialog(
                            title=f"Confirm Deletion",
                            message=f"Are you sure you want to delete {item_repr}?",
                            confirm_text="Delete",
                        )
                        if confirmed:
                            deleted = await self.api_client.delete(
                                current_plural_name, item_id
                            )
                            if deleted:
                                await load_data()  # Refresh table

                    # --- Dialogs ---
                    create_dialog = ui.dialog().props(
                        "persistent"
                    )  # Prevent closing on outside click
                    edit_dialog = ui.dialog().props("persistent")

                    def show_create_dialog():
                        with (
                            create_dialog,
                            ui.card().classes("w-full max-w-lg"),
                        ):  # Limit dialog width
                            ui.label(f"Create New {current_model.__name__}").classes(
                                "text-h6"
                            )
                            entity_form(
                                model=current_model,
                                id_field=self.id_field,
                                on_save=handle_save_create,
                                on_cancel=create_dialog.close,
                            )
                        create_dialog.open()

                    async def show_edit_dialog(item_id: Any):
                        # Fetch fresh data for editing to avoid stale data
                        item_data = await self.api_client.get_one(
                            current_plural_name, item_id
                        )
                        if not item_data:
                            # API client should have shown a notification
                            return

                        with (
                            edit_dialog,
                            ui.card().classes("w-full max-w-lg"),
                        ):  # Limit dialog width
                            ui.label(
                                f"Edit {current_model.__name__} (ID: {item_id})"
                            ).classes("text-h6")
                            entity_form(
                                model=current_model,
                                id_field=self.id_field,
                                initial_data=item_data,
                                on_save=lambda data: handle_save_edit(item_id, data),
                                on_cancel=edit_dialog.close,
                            )
                        edit_dialog.open()

                    # --- Page Layout ---
                    with (
                        ui.header(elevated=True)
                        .style("background-color: #3874c8")
                        .classes("items-center justify-between")
                    ):
                        with ui.row().classes("items-center"):
                            # Simple navigation (can be turned into a reusable component)
                            ui.label("CRUD GUI").classes("text-h6")
                            with ui.tabs() as tabs:
                                for name, path in nav_links.items():
                                    tab = ui.tab(
                                        label=name, name=path
                                    )  # Tab name = entity name
                            # Navigate on tab change
                            tabs.on(
                                "update:model-value",
                                lambda e: ui.navigate.to(e.sender.value),
                            )  # e.value holds the 'value' of the tab (path)
                            # Set initial tab based on current path
                            tabs.set_value(page_path)

                    with ui.column().classes("w-full q-pa-md"):  # Add padding
                        with ui.row().classes("w-full items-center q-mb-md"):
                            ui.label(current_page_title).classes("text-h5")
                            ui.space()
                            ui.button(icon="refresh", on_click=load_data).props(
                                "flat dense round"
                            )

                        # Generate columns for the table
                        columns = self._generate_ui_columns(current_model)

                        # Render the entity table component
                        # Store table reference to allow programmatic updates
                        table_ref = entity_table(
                            columns=columns,
                            rows=items,  # Initial data (empty at first)
                            id_field=self.id_field,
                            on_create=show_create_dialog,
                            on_edit=show_edit_dialog,
                            on_delete=handle_delete,
                        )

                    # --- Initial Data Load ---
                    await load_data()  # Load data when the page is first accessed

                    # --- Cleanup on disconnect (optional but good practice) ---
                    # ui.on('disconnect', self.api_client.close) # Close client when browser tab closes

            # Actually register the function created by create_page
            create_page(model, plural_name, page_title)
            print(f"  - Generated NiceGUI page at: {page_path}")

        print("NiceGUI page generation complete.")

    def attach_to_app(
        self, app: FastAPI, storage_secret: Optional[str] = "a_secure_secret_key"
    ):
        """Mounts the NiceGUI pages onto the FastAPI application."""
        if not storage_secret:
            print(
                "Warning: No storage_secret provided for NiceGUI. Using a default key. Please set a strong secret in production."
            )
            storage_secret = "a_secure_secret_key"  # Default fallback, CHANGE THIS

        print(
            f"Attaching NiceGUI to FastAPI app. GUI accessible at '{self.page_prefix}'"
        )
        ui.run_with(
            app,
            mount_path=f"/{self.page_prefix}",
            title="Auto CRUD App",  # Default title for pages without specific one
            storage_secret=storage_secret,  # Needed for session management
            # Add other ui.run options if needed (e.g., favicon)
        )

    def run(self, *args, **kwargs):
        ui.run(*args, **kwargs)
