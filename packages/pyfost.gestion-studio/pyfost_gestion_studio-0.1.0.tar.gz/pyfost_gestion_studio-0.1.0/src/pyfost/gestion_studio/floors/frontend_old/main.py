from typing import Any
from pathlib import Path
import importlib
import inspect
import json
from datetime import datetime

from nicegui import ui, app, events, Client  # Import Client for storage access

import api_client  # Your API client
from shared_state import (
    init_shared_state,
    get_selected_items,
    get_selected_item_type,
    register_right_drawer_updater,
    clear_selection,
)

# Define Views - Add entries for each view module you create
# ('route', 'module_name', 'display_name', 'icon')
VIEWS = [
    ("/", "home", "Home", "home"),  # Add a simple home view maybe
    ("/facilities", "facilities", "Facilities", "business"),
    ("/floors", "floors", "Floors", "stairs"),
    ("/resources", "resources", "Resources", "memory"),
    ("/assignments", "assignments", "Assignments", "event_seat"),  # Example route
    ("/tasks", "tasks", "Tasks", "list_alt"),
    # Add floors, seats views as needed (maybe nested navigation?)
]

# --- Right Drawer Multi-Edit Logic (Simplified Example) ---

# Placeholder values for multi-selection display
MULTIPLE_VALUES = object()  # Unique object to represent multiple values


def get_common_value(items: list[dict], key: str) -> Any:
    """Checks if all items have the same value for a key."""
    if not items:
        return None
    first_value = items[0].get(key)
    for item in items[1:]:
        if item.get(key) != first_value:
            return MULTIPLE_VALUES  # Return placeholder if values differ
    return first_value


async def update_multiple_items(items: list[dict], item_type: str, update_data: dict):
    """Calls API to update multiple items (simplified: updates one by one)."""
    # In a real app, consider a bulk API endpoint if available
    success_count = 0
    errors = []
    item_id_key = "id"  # Assuming 'id' is the primary key

    # Determine the correct update function based on type
    update_func = None
    if item_type == "resource":
        update_func = api_client.update_resource
    elif item_type == "task":
        update_func = api_client.update_task
    # Add other types...

    if not update_func:
        raise ValueError(f"Update function not defined for type: {item_type}")

    if not update_data:
        ui.notify("No changes detected.", type="info")
        return

    for item in items:
        item_id = item.get(item_id_key)
        if item_id is None:
            errors.append(f"Item missing ID: {item}")
            continue
        try:
            await update_func(item_id, update_data)
            success_count += 1
        except Exception as e:
            errors.append(f"Failed to update item {item_id}: {e}")

    if success_count > 0:
        ui.notify(f"Successfully updated {success_count} item(s).", type="positive")
    if errors:
        # Show first few errors, log the rest
        error_msg = f"Encountered {len(errors)} error(s): {'; '.join(errors[:3])}{'...' if len(errors) > 3 else ''}"
        print("Bulk update errors:", errors)
        ui.notify(error_msg, type="negative", multi_line=True)


# --- Application Setup ---


@ui.page("/")  # Root path, can redirect or show a welcome message
async def home_page(client: Client):
    setup_ui_layout(client)  # Build the main layout
    with ui.column().classes("absolute-center items-center"):
        ui.icon("workspaces", size="xl", color="primary")
        ui.label("Welcome to Workplace Seat Management").classes(
            "text-h4 text-grey-8 q-mt-md"
        )
        ui.label("Select a view from the left menu to get started.").classes(
            "text-subtitle1 text-grey-6"
        )


# # Dynamically create pages for each view defined in VIEWS
# def create_view_pages():
#     views_path = Path(__file__).parent / "views"
#     for route, module_name, display_name, icon in VIEWS:
#         if route == "/":
#             continue  # Skip home page, already defined

#         module_path = views_path / f"{module_name}.py"
#         if module_path.exists():
#             # Dynamically import the view module
#             spec = importlib.util.spec_from_file_location(
#                 f"views.{module_name}", module_path
#             )
#             view_module = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(view_module)

#             # Find the function responsible for creating the UI (convention: create_ui)
#             create_ui_func = getattr(view_module, "create_ui", None)

#             if callable(create_ui_func):
#                 # Decorate the function with ui.page
#                 decorated_func = ui.page(route)(create_ui_func)

#                 # Wrap it to also set up the main layout
#                 async def page_wrapper(
#                     func=decorated_func, client: Client = None
#                 ):  # Need client for storage
#                     setup_ui_layout(client)  # Ensure layout exists on direct navigation
#                     await func()

#                 # Re-register with the route using the wrapper
#                 # Note: This dynamic registration method might need adjustment based on NiceGUI version/internals
#                 # A simpler way might be to define all @ui.page decorators directly in main.py
#                 # and call the view creation functions from there. Let's try that instead for robustness:

#                 # --> Alternative: Define page routes here and call view functions <--
#                 # @ui.page(route)
#                 # async def generated_page(client: Client, func=create_ui_func):
#                 #      setup_ui_layout(client)
#                 #      await func()

#             else:
#                 print(
#                     f"Warning: Module 'views/{module_name}.py' does not have a callable 'create_ui' function."
#                 )
#         else:
#             print(f"Warning: View module 'views/{module_name}.py' not found.")


# --> Define pages explicitly for better control <--
@ui.page("/facilities")
async def facilities_page(client: Client):
    setup_ui_layout(client)
    from views import (
        facilities,
    )  # Import here to avoid circular dependency issues at top level

    await facilities.create_ui()


@ui.page("/floors")
async def floors_page(client: Client):
    setup_ui_layout(client)
    from views import (
        floors,
    )  # Import here to avoid circular dependency issues at top level

    await floors.create_ui()


@ui.page("/resources")
async def resources_page(client: Client):
    setup_ui_layout(client)
    from views import resources  # Import specific view module

    await resources.create_ui()  # Call its creation function


@ui.page("/assignments")
async def assignments_page(client: Client):
    setup_ui_layout(client)
    from views import assignments

    await assignments.create_ui()


@ui.page("/tasks")
async def tasks_page(client: Client):
    setup_ui_layout(client)
    from views import tasks

    await tasks.create_ui()


# Add other @ui.page decorators for your views here...


# --- Main UI Layout Function ---
# This function builds the header, drawers, footer ONCE per client connection
# It uses client.connect handlers or checks client.has_socket() if needed,
# but simply calling it at the start of each @ui.page function works too.
def setup_ui_layout(client: Client):
    # Initialize state on first connection for this client
    client.on_connect(init_shared_state)

    # --- Check if layout already exists for this client ---
    # NiceGUI renders elements once per client unless explicitly updated.
    # We check if the header (as a proxy for the layout) exists in the client's element tree.
    # This prevents adding duplicate headers/drawers on page navigation within the SPA.
    if 0 and client.has_element("main_header"):
        # print("Layout already exists for client.") # Debug
        return  # Layout already built for this client session

    # print("Setting up UI layout for client.") # Debug

    # --- Header ---
    # Add an ID to check for existence later
    with (
        ui.header(elevated=True)
        .classes("bg-primary text-white justify-between")
        .props("reveal")
        # .set_client_id("main_header")
    ):
        with ui.row().classes("items-center"):
            ui.button(icon="menu", on_click=lambda: left_drawer.toggle()).props(
                "flat color=white"
            )
            # Use an appropriate icon - maybe 'workspaces' or find a logo image
            ui.icon("workspaces", size="lg").classes("q-mr-sm")
            ui.label("Workplace Management").classes("text-h6")

        # Placeholder for potential header tools/user info
        with ui.row().classes("items-center"):
            # --- Export/Import Menu ---
            with ui.button(icon="settings").props("flat color=white"):
                with ui.menu() as menu:

                    async def handle_export():
                        try:
                            data = await api_client.export_data()
                            # Convert dict to JSON string for download
                            json_data = json.dumps(data, indent=4)
                            # Trigger browser download
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"workplace_backup_{timestamp}.json"
                            ui.download(
                                content=json_data.encode("utf-8"),
                                filename=filename,
                                media_type="application/json",
                            )
                            ui.notify("Data prepared for download.", type="positive")
                        except Exception as e:
                            ui.notify(f"Export failed: {e}", type="negative")
                        menu.close()  # Close menu after action

                    ui.menu_item("Export Data", on_click=handle_export)

                    async def handle_upload(e: events.UploadEventArguments):
                        try:
                            content_bytes = await e.content.read()
                            data_to_import = json.loads(content_bytes.decode())
                            # Confirmation Dialog
                            with ui.dialog() as confirm_import_dialog, ui.card():
                                ui.label("Confirm Import").classes("text-h6")
                                ui.label(
                                    "WARNING: This will replace ALL existing data in the system. This action cannot be undone."
                                ).classes("text-negative")
                                with ui.row():

                                    async def do_import():
                                        confirm_import_dialog.close()  # Close dialog first
                                        try:
                                            result = await api_client.import_data(
                                                data_to_import
                                            )
                                            ui.notify(
                                                result.get(
                                                    "message", "Import successful!"
                                                ),
                                                type="positive",
                                            )
                                            # Optionally force a page reload or navigate home after import
                                            # ui.navigate.to('/') # Navigate home
                                            # ui.navigate.reload() # Force full reload
                                        except Exception as import_err:
                                            ui.notify(
                                                f"Import failed: {import_err}",
                                                type="negative",
                                                multi_line=True,
                                            )

                                    ui.button(
                                        "Confirm Import",
                                        on_click=do_import,
                                        color="negative",
                                    )
                                    ui.button(
                                        "Cancel", on_click=confirm_import_dialog.close
                                    )
                            confirm_import_dialog.open()

                        except json.JSONDecodeError:
                            ui.notify("Invalid JSON file.", type="negative")
                        except Exception as upload_err:
                            ui.notify(
                                f"Error processing import file: {upload_err}",
                                type="negative",
                            )
                        finally:
                            menu.close()  # Close menu after action

                    # Use ui.upload for the import action
                    ui.upload(
                        label="Import Data",
                        on_upload=handle_upload,
                        auto_upload=True,  # Upload immediately after selection
                        max_file_size=50_000_000,  # 50MB limit example
                    ).props("flat dense no-caps text-color=black").classes("w-full")
                    # Styling might need adjustment for menu items

    # --- Left Drawer (Navigation) ---
    with ui.left_drawer(value=True, elevated=True).classes("bg-grey-2") as left_drawer:
        # ui.label("Views").classes("text-h6 q-pa-md")
        # ui.separator()
        with ui.list():
            for route, module_name, display_name, icon in VIEWS:
                # Link navigates using NiceGUI's router
                with ui.item(
                    # clickable=True,
                    on_click=lambda r=route: ui.navigate.to(r),
                ):
                    with ui.item_section().props("avatar"):
                        ui.icon(icon)
                    with ui.item_section():
                        ui.label(display_name)

    # --- Right Drawer (Editor/Details) ---
    with ui.right_drawer(value=False, fixed=False, elevated=True).classes(
        "bg-grey-1 q-pa-md"
    ) as right_drawer:
        # Content will be dynamically added here by update_right_drawer_content
        right_drawer_content_area = ui.column().classes("w-full")

    # Function to update right drawer content based on shared_state
    def update_right_drawer_content():
        items = get_selected_items()
        item_type = get_selected_item_type()
        right_drawer_content_area.clear()  # Clear previous content

        if not items:
            right_drawer.value = False  # Close drawer if nothing selected
            return

        right_drawer.value = True  # Open drawer

        with right_drawer_content_area:
            count = len(items)
            ui.label(
                f"{count} {item_type.capitalize()}{'s' if count > 1 else ''} selected"
            ).classes("text-h6 q-mb-md")
            ui.separator()

            # --- Build Editor Form based on type ---
            if item_type == "facility":
                build_facility_editor(items)
            elif item_type == "resource":
                build_resource_editor(items)
            # Add elif for 'seat', 'assignment', 'task' etc.
            elif item_type == "task":
                build_task_editor(items)
            else:
                ui.label(f"Editing for '{item_type}' not implemented yet.")

            # Add common actions
            ui.separator().classes("q-mt-md")
            with ui.row().classes("justify-end w-full q-mt-sm"):
                ui.button("Close", on_click=lambda: clear_selection()).props(
                    "flat"
                )  # Clear selection closes drawer

    # Register the updater function with shared state
    register_right_drawer_updater(update_right_drawer_content)

    # --- Editor Form Builders (Examples) ---
    def build_facility_editor(items: list[dict]):
        """Builds the editor form for Facility items."""
        count = len(items)
        # Assume facilities only have 'name' editable here
        name_val = get_common_value(items, "name")

        with ui.card() as form:  # Use a form for potential validation later
            name_input = ui.input("Facility Name")
            if name_val is MULTIPLE_VALUES:
                name_input.props('placeholder="(Multiple Values)"')
                name_input.classes(
                    "input-multiple-values"
                )  # Add custom class for styling
            else:
                name_input.value = name_val

            # Add Save/Update button - Needs implementation
            async def save_changes():
                ui.notify("Facility update not implemented yet.")  # Placeholder
                # Get new_name = name_input.value
                # If new_name is different from original common value OR MULTIPLE_VALUES
                # Call update_multiple_items(items, 'facility', {'name': new_name})
                # Refresh source table...

            ui.button("Save Changes", on_click=save_changes).props(
                "color=primary q-mt-md"
            )

    def build_resource_editor(items: list[dict]):
        """Builds the editor form for Resource items."""
        count = len(items)
        # Editable fields: identifier (maybe not?), category, properties
        identifier_val = get_common_value(items, "identifier")
        category_val = get_common_value(items, "resource_category")
        # Properties are complex - maybe show JSON editor or specific fields?

        with ui.card() as form:
            # Identifier might be read-only after creation
            ui.input("Identifier").bind_value_from(
                items[0] if count == 1 else {}, "identifier"
            ).props(
                f"readonly disable={count > 1 and identifier_val is MULTIPLE_VALUES}"
            )  # Readonly, disable if multiple differ
            if count > 1 and identifier_val is MULTIPLE_VALUES:
                ui.tooltip("Cannot change identifier for multiple different resources.")

            # Category Selection
            # Get categories from API model/enum if possible, hardcode for now
            categories = ["User", "Workstation", "SoftwareLicense", "Other"]
            cat_select = ui.select(categories, label="Category")
            if category_val is MULTIPLE_VALUES:
                cat_select.props('placeholder="(Multiple Values)"')
            else:
                cat_select.value = category_val

            # Properties Editor (Simple Example: Text Area)
            # A proper editor would parse the JSON and show fields
            prop_val = get_common_value(items, "properties")
            prop_input = ui.textarea("Properties (JSON)")
            if prop_val is MULTIPLE_VALUES:
                prop_input.props('placeholder="(Multiple Values - Edit with caution)"')
                prop_input.value = "{}"  # Default to empty JSON object on edit
            else:
                # Pretty print JSON for display
                prop_input.value = json.dumps(prop_val or {}, indent=2)

            # Save Button
            async def save_changes():
                update_payload = {}
                new_category = cat_select.value
                new_props_str = prop_input.value

                if new_category and new_category != category_val:
                    update_payload["resource_category"] = (
                        new_category  # API schema uses resource_category
                    )

                try:
                    new_props = json.loads(new_props_str)
                    # Only include properties if they changed or were multiple values
                    if prop_val is MULTIPLE_VALUES or new_props != prop_val:
                        update_payload["properties"] = new_props
                except json.JSONDecodeError:
                    ui.notify("Invalid JSON in properties.", type="warning")
                    return  # Don't save if JSON is bad

                if not update_payload:
                    ui.notify("No changes detected.", type="info")
                    return

                # Confirmation for multi-update
                if count > 1:
                    with ui.dialog() as confirm_dialog, ui.card():
                        ui.label(f"Update {count} resources?").classes("text-h6")
                        if "resource_category" in update_payload:
                            ui.label(
                                f"Set Category to: {update_payload['resource_category']}"
                            )
                        if "properties" in update_payload:
                            ui.label("Update Properties")
                        with ui.row():
                            ui.button(
                                "Confirm Update",
                                color="primary",
                                on_click=lambda: confirm_dialog.submit(True),
                            )
                            ui.button(
                                "Cancel", on_click=lambda: confirm_dialog.submit(False)
                            )
                    confirmed = await confirm_dialog
                    if not confirmed:
                        return

                try:
                    await update_multiple_items(items, "resource", update_payload)
                    # Need to trigger refresh of the source table in the view
                    # This requires communication back to the view (e.g., via app events or callbacks)
                    app.storage.client["refresh_trigger"] = (
                        datetime.now()
                    )  # Example trigger
                    clear_selection()  # Close drawer after save
                except Exception as e:
                    ui.notify(f"Error updating resource(s): {e}", type="negative")

            ui.button("Save Changes", on_click=save_changes).props(
                "color=primary q-mt-md"
            )

    def build_task_editor(items: list[dict]):
        """Builds the editor form for Task items."""
        count = len(items)
        status_val = get_common_value(items, "status")
        assignee_val = get_common_value(items, "assignee")
        notes_val = get_common_value(items, "notes")

        task_statuses = [
            "Pending",
            "In Progress",
            "Completed",
            "Blocked",
        ]  # From backend Enum

        with ui.form() as form:
            ui.label(
                f"Task Type: {get_common_value(items, 'task_type') or '(Multiple Types)'}"
            ).classes(
                "text-caption"
            )  # Readonly type

            status_select = ui.select(task_statuses, label="Status")
            if status_val is MULTIPLE_VALUES:
                status_select.props('placeholder="(Multiple Statuses)"')
            else:
                status_select.value = status_val

            assignee_input = ui.input("Assignee")
            if assignee_val is MULTIPLE_VALUES:
                assignee_input.props('placeholder="(Multiple Assignees)"')
            else:
                assignee_input.value = assignee_val

            notes_input = ui.textarea("Notes")
            if notes_val is MULTIPLE_VALUES:
                notes_input.props(
                    'placeholder="(Multiple Notes - Content will overwrite)"'
                )
            else:
                notes_input.value = notes_val

            async def save_changes():
                update_payload = {}
                if status_select.value and status_select.value != status_val:
                    update_payload["status"] = status_select.value
                # Handle assignee and notes updates similarly, checking if changed from common value or if MULTIPLE_VALUES
                new_assignee = assignee_input.value
                if new_assignee is not None and (
                    assignee_val is MULTIPLE_VALUES or new_assignee != assignee_val
                ):
                    update_payload["assignee"] = new_assignee

                new_notes = notes_input.value
                if new_notes is not None and (
                    notes_val is MULTIPLE_VALUES or new_notes != notes_val
                ):
                    update_payload["notes"] = new_notes

                if not update_payload:
                    ui.notify("No changes detected.", type="info")
                    return

                # Add multi-update confirmation if count > 1... (similar to resource editor)
                # ... confirmation dialog logic ...
                confirmed = True  # Assume confirmed for brevity
                if not confirmed:
                    return

                try:
                    await update_multiple_items(items, "task", update_payload)
                    app.storage.client["refresh_trigger"] = (
                        datetime.now()
                    )  # Trigger refresh
                    clear_selection()
                except Exception as e:
                    ui.notify(f"Error updating task(s): {e}", type="negative")

            ui.button("Save Changes", on_click=save_changes).props(
                "color=primary q-mt-md"
            )

    # --- Footer ---
    # Use ui.footer for consistency, or page_sticky if preferred
    with ui.footer().classes("bg-grey-3 text-grey-7"):
        ui.label("Made with ♥️ by Dee909").classes("text-caption q-pa-sm")


# --- Run the app ---
# Create the view pages dynamically before running
# create_view_pages() # Call the dynamic function (or use explicit @ui.page)

# Add CORS headers if backend and frontend are on different origins during development
# This should ideally be handled in the FastAPI backend CORS middleware
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Note: NiceGUI doesn't run FastAPI middleware directly. Backend needs CORS.

ui.run(
    title="Workplace Manager",
    storage_secret="SOME_SECRET_KEY_FOR_USER_STORAGE",
    port=8909,
    reload=True,
)
