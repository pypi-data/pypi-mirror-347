from nicegui import ui, app, events
from typing import List, Dict, Any, Optional
import json  # For displaying properties JSON

import api_client  # Your API client
from shared_state import set_selected_items, clear_selection  # Import selection handler

# Define resource categories including an "All" option for filtering
# Should ideally match the ResourceCategoryEnum from the backend + 'All'
RESOURCE_CATEGORIES = ["All", "User", "Workstation", "SoftwareLicense", "Other"]

# Define columns for the table
columns = [
    {
        "name": "id",
        "label": "ID",
        "field": "id",
        "sortable": True,
        "align": "left",
        "style": "width: 50px",
    },
    {
        "name": "identifier",
        "label": "Identifier",
        "field": "identifier",
        "required": True,
        "sortable": True,
        "align": "left",
    },
    {
        "name": "resource_category",
        "label": "Category",
        "field": "resource_category",
        "sortable": True,
        "align": "left",
    },
    # Properties column needs custom display logic
    {
        "name": "properties",
        "label": "Properties",
        "field": "properties",
        "align": "left",
        "sortable": False,
    },
    {"name": "actions", "label": "Actions", "field": "actions", "align": "right"},
]


# --- Helper for Properties Display ---
def format_properties(props: Optional[Dict]) -> str:
    """Formats the properties dictionary for display in the table."""
    if not props:
        return ""
    try:
        # Simple JSON string representation, could be more elaborate
        return json.dumps(props, indent=2)
    except Exception:
        return str(props)  # Fallback


async def create_ui():
    """Creates the UI for the Resources view."""
    print("Creating Resources UI")  # Debug print

    # --- State ---
    resources: List[Dict[str, Any]] = []
    selected: List[Dict[str, Any]] = []  # Bound to table selection
    # Default pagination settings for ui.table
    pagination = {"page": 1, "rowsPerPage": 10}  # or load from user preference

    # --- Data Fetching and Refresh Logic ---
    async def refresh_resources():
        """Fetches resources from API based on filter and updates the table."""
        nonlocal resources
        loading_indicator.visible = True
        table.props("loading=true")  # Show table's built-in loading
        # Get current filter value, None if "All" is selected
        category_filter = (
            filter_category_select.value
            if filter_category_select.value != "All"
            else None
        )
        try:
            print(f"Refreshing resources with category: {category_filter}")
            # Fetch ALL resources matching the filter.
            # NiceGUI table handles pagination display client-side based on fetched rows.
            # If datasets become huge, backend pagination is required.
            fetched_resources = await api_client.get_resources(category=category_filter)
            resources[:] = fetched_resources  # Update the list in-place for reactivity
            table.rows = resources  # Assign potentially new list object to rows

            # Clear selection when table refreshes
            selected.clear()
            table.selected.clear()
            set_selected_items([], None)  # Clear global selection
            table.update()  # Explicitly update table component
            print(f"Found {len(resources)} resources.")
            ui.notify(f"Loaded {len(resources)} resources.", type="info", timeout=2000)
        except Exception as e:
            ui.notify(f"Error fetching resources: {e}", type="negative")
        finally:
            loading_indicator.visible = False
            table.props("loading=false")  # Hide table loading

    # --- UI Elements ---
    with ui.column().classes("w-full gap-4"):
        # --- Header Row ---
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Manage Resources").classes("text-h5")
            loading_indicator = ui.spinner("dots", size="lg", color="primary").props(
                "flat"
            )
            with ui.row().classes("items-center"):
                ui.button(
                    "Add Resource", on_click=lambda: add_dialog.open(), icon="add"
                )
                ui.button("Refresh", on_click=refresh_resources, icon="refresh")

        # --- Filter Row ---
        with ui.row().classes("w-full items-center"):
            filter_category_select = ui.select(
                RESOURCE_CATEGORIES,
                value="All",
                label="Filter by Category",
                on_change=refresh_resources,  # Refresh data when filter changes
            ).classes("w-48")
            # Add more filters here if needed (e.g., search by identifier)

        # --- Table ---
        # Use bind_rows for reactivity if manipulating the list directly
        table = (
            ui.table(
                columns=columns,
                rows=[],  # Initially empty, populated by refresh_resources
                row_key="id",
                selection="multiple",
                pagination=pagination,  # Pass pagination state object
                on_select=lambda e: set_selected_items(
                    e.selection, "resource"
                ),  # Update global state
            ).classes("w-full")
            # .bind_selected(selected)
        )

        # Custom slot for 'Properties' column display
        table.add_slot(
            "body-cell-properties",
            r"""
            <q-td :props="props" key="properties">
                <!-- Use pre for formatted JSON, add styling for overflow -->
                <pre class="text-caption bg-grey-2 q-pa-xs rounded-borders overflow-auto" style="max-height: 100px; white-space: pre-wrap; word-break: break-all;">{{ props.row.properties_formatted }}</pre>
                <!-- Optional: Add a tooltip/dialog for full view -->
                <q-tooltip v-if="props.row.properties_formatted?.length > 100">
                    Click to see full properties (Not Implemented)
                </q-tooltip>
            </q-td>
        """,
        )

        # Add action buttons to each row
        table.add_slot(
            "body-cell-actions",
            """
            <q-td :props="props" key="actions" style="width: 1px; padding-right: 16px;"> <!-- Minimize width -->
                <q-btn flat dense round icon="delete" color="negative" @click="() => $parent.$emit('delete', props.row)"/>
            </q-td>
        """,
        )

        # Handle delete action emitted from table slot
        table.on("delete", lambda e: confirm_delete(e.args))

    # --- Dialogs ---
    # Add Dialog
    with ui.dialog() as add_dialog, ui.card().classes("min-w-[400px]"):
        ui.label("Add New Resource").classes("text-h6")
        # Use a form for better structure and potential validation
        with ui.card().classes("flex flex-col gap-2") as add_form:
            identifier_input = ui.input(
                "Identifier *",
                validation={"Identifier is required": lambda v: bool(v and v.strip())},
            ).props("autofocus outlined dense")
            category_select = ui.select(
                options=[
                    cat for cat in RESOURCE_CATEGORIES if cat != "All"
                ],  # Exclude "All"
                label="Category *",
                with_input=False,  # Or True if you want custom categories?
                validation={"Category is required": lambda v: v is not None},
            ).props("outlined dense")
            properties_input = (
                ui.textarea("Properties (JSON format)")
                .props("outlined dense")
                .classes("text-mono")
            )

            async def handle_add():
                # TODO: implement form validation:
                # if not await add_form.validate():
                #     ui.notify("Please fill in required fields.", type="warning")
                #     return

                identifier = identifier_input.value.strip()
                category = category_select.value
                properties_str = properties_input.value.strip()
                properties_dict = None

                if properties_str:
                    try:
                        properties_dict = json.loads(properties_str)
                        if not isinstance(properties_dict, dict):
                            raise ValueError(
                                "Properties must be a JSON object (dictionary)."
                            )
                    except Exception as json_e:
                        ui.notify(
                            f"Invalid JSON in Properties: {json_e}", type="warning"
                        )
                        return  # Stop if JSON is invalid

                try:
                    await api_client.create_resource(
                        identifier=identifier,
                        category=category,
                        properties=properties_dict,
                    )
                    ui.notify(
                        f'Resource "{identifier}" created successfully!',
                        type="positive",
                    )
                    add_dialog.close()
                    # Reset form (important after successful add)
                    identifier_input.value = ""
                    category_select.value = None
                    properties_input.value = ""
                    await refresh_resources()  # Refresh table
                except Exception as e:
                    ui.notify(
                        f"Error creating resource: {e}",
                        type="negative",
                        multi_line=True,
                    )

            with ui.row().classes("justify-end w-full"):
                ui.button("Create", on_click=handle_add).props("color=primary")
                ui.button("Cancel", on_click=add_dialog.close)

    # Delete Confirmation Dialog
    async def confirm_delete(resource_to_delete: Dict[str, Any]):
        with ui.dialog() as confirm_dialog, ui.card():
            ui.label(f"Delete Resource?").classes("text-h6")
            ui.label(
                f'Are you sure you want to delete resource "{resource_to_delete.get("identifier", "N/A")}" (ID: {resource_to_delete.get("id", "N/A")})?'
            )
            ui.label(
                "This might affect existing assignments using this resource!"
            ).classes("text-warning")
            with ui.row().classes("justify-end w-full"):

                async def do_delete():
                    try:
                        await api_client.delete_resource(resource_to_delete["id"])
                        ui.notify(
                            f'Resource "{resource_to_delete.get("identifier", "")}" deleted.',
                            type="positive",
                        )
                        confirm_dialog.close()
                        await refresh_resources()
                    except Exception as e:
                        ui.notify(
                            f"Error deleting resource: {e}",
                            type="negative",
                            multi_line=True,
                        )
                        confirm_dialog.close()  # Close even on error

                ui.button("Delete", on_click=do_delete, color="negative")
                ui.button("Cancel", on_click=confirm_dialog.close)
        confirm_dialog.open()

    # --- Handle Refresh Trigger from Right Drawer (if needed) ---
    async def handle_potential_refresh():
        """Checks if a refresh was triggered externally (e.g., by right drawer save)."""
        trigger_time = app.storage.client.get("refresh_trigger")
        last_refresh = getattr(
            handle_potential_refresh, "last_refresh_trigger_time", None
        )

        if trigger_time and trigger_time != last_refresh:
            print("Refresh triggered externally for resources view.")
            handle_potential_refresh.last_refresh_trigger_time = trigger_time
            await refresh_resources()

    # Periodically check for the refresh trigger
    # Adjust interval as needed, or use a more direct event system if built
    ui.timer(2.0, handle_potential_refresh, active=True)

    # --- Initial Data Load ---
    # Prepare data structure for table slots *before* initial load
    # (Doing this in refresh_resources might be better)
    def prepare_rows_for_display(rows: List[Dict]) -> List[Dict]:
        for row in rows:
            row["properties_formatted"] = format_properties(row.get("properties"))
        return rows

    # Make refresh_resources also call prepare_rows_for_display
    # Let's modify refresh_resources slightly
    async def refresh_resources_and_prepare():
        """Fetches resources, prepares them for display, and updates the table."""
        nonlocal resources
        loading_indicator.visible = True
        table.props("loading=true")
        category_filter = (
            filter_category_select.value
            if filter_category_select.value != "All"
            else None
        )
        try:
            print(f"Refreshing resources with category: {category_filter}")
            fetched_resources = await api_client.get_resources(category=category_filter)
            prepared_resources = prepare_rows_for_display(
                fetched_resources
            )  # Prepare here
            resources[:] = prepared_resources  # Update state list
            table.rows = resources  # Assign to table

            selected.clear()
            table.selected.clear()
            set_selected_items([], None)
            table.update()
            print(f"Found and prepared {len(resources)} resources.")
            # ui.notify(f"Loaded {len(resources)} resources.", type='info', timeout=2000) # Avoid double notify
        except Exception as e:
            ui.notify(f"Error fetching resources: {e}", type="negative")
            # Ensure table rows are empty on error? Or keep stale data?
            # resources[:] = []
            # table.rows = resources
            # table.update()
        finally:
            loading_indicator.visible = False
            table.props("loading=false")

    if 0:
        pass
        # NEEDS CLEANUP

        # # Replace previous refresh calls with the new wrapper function
        # filter_category_select.on_change=refresh_resources_and_prepare
        # add_dialog.on_dismiss(refresh_resources_and_prepare) # Refresh after add potentially
        # # Need to update delete handler to call the wrapper too
        # # Re-define confirm_delete slightly to use the wrapper
        # async def confirm_delete(resource_to_delete: Dict[str, Any]):
        #     # ... (dialog definition as before) ...
        #             async def do_delete():
        #                 try:
        #                     await api_client.delete_resource(resource_to_delete['id'])
        #                     ui.notify(f'Resource "{resource_to_delete.get("identifier", "")}" deleted.', type='positive')
        #                     confirm_dialog.close()
        #                     await refresh_resources_and_prepare() # <--- Use wrapper here
        #                 except Exception as e:
        #                     ui.notify(f"Error deleting resource: {e}", type='negative', multi_line=True)
        #                     confirm_dialog.close()
        #     # ... (rest of confirm_delete) ...
        #     confirm_dialog.open()

    # Use ui.timer for initial load after UI is built
    ui.timer(
        0.1, refresh_resources_and_prepare, once=True
    )  # Use wrapper for initial load
