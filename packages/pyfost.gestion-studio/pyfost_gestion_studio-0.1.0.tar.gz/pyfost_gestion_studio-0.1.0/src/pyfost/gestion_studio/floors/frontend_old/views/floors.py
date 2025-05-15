from nicegui import ui, app
from typing import List, Dict, Any
import api_client
from shared_state import set_selected_items

# Define columns for the table
columns = [
    {
        "name": "id",
        "label": "ID",
        "field": "id",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "level",
        "label": "Floor Name",
        "field": "level",
        "required": True,
        "sortable": True,
        "align": "left",
    },
    # Add more columns if needed (e.g., number of floors - requires API change)
    {
        "name": "actions",
        "label": "Actions",
        "field": "actions",
        "align": "right",
    },
]


async def create_ui():
    """Creates the UI for the Floors view."""
    print("Creating Floors UI")  # Debug print

    # State for table data and selection
    floors: List[Dict[str, Any]] = []
    selected: List[Dict[str, Any]] = []  # Bound to table selection

    async def refresh_floors():
        """Fetches floors from API and updates the table."""
        nonlocal floors
        try:
            print("Refreshing floors...")
            floors = await api_client.get_floors_for_facility(1)
            table.rows = floors
            # Clear selection when table refreshes to avoid stale data in right drawer
            # Or implement more complex logic to preserve selection if items still exist
            selected.clear()
            table.selected.clear()
            set_selected_items([], None)  # Clear global selection
            table.update()
            print(f"Found {len(floors)} floors.")
        except Exception as e:
            ui.notify(f"Error fetching facilities: {e}", type="negative")
        loading_indicator.visible = False

    # --- UI Elements ---
    with ui.column().classes("w-full"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Manage Facilities").classes("text-h5")
            loading_indicator = ui.spinner("dots", size="lg", color="primary")
            with ui.row():
                ui.button(
                    "Add Facility", on_click=lambda: add_dialog.open(), icon="add"
                )
                ui.button("Refresh", on_click=refresh_floors, icon="refresh")

        # Table
        table = (
            ui.table(
                columns=columns,
                rows=floors,
                row_key="id",
                selection="multiple",
                on_select=lambda e: set_selected_items(
                    e.selection, "facility"
                ),  # Update global state on select
            ).classes("w-full")
            # .bind_selected(selected)
        )
        table.set_selection("multiple")

        # Add action buttons to each row
        table.add_slot(
            "body-cell-actions",
            """
            <q-td :props="props" key="actions">
                <q-btn flat dense round icon="delete" color="negative" @click="() => $parent.$emit('delete', props.row)"/>
                <!-- Add edit button if needed -->
            </q-td>
        """,
        )

        # Handle delete action emitted from table slot
        table.on("delete", lambda e: confirm_delete(e.args))

    # --- Dialogs ---
    # Add Dialog
    with ui.dialog() as add_dialog, ui.card():
        ui.label("Add New Facility").classes("text-h6")
        name_input = ui.input("Facility Name").props("autofocus")

        async def handle_add():
            name = name_input.value.strip()
            if not name:
                ui.notify("Facility name cannot be empty.", type="warning")
                return
            try:
                await api_client.create_facility(name=name)
                ui.notify(f'Facility "{name}" created successfully!', type="positive")
                add_dialog.close()
                await refresh_floors()  # Refresh table
            except Exception as e:
                ui.notify(f"Error creating facility: {e}", type="negative")

        with ui.row():
            ui.button("Create", on_click=handle_add)
            ui.button("Cancel", on_click=add_dialog.close)

    # Delete Confirmation Dialog
    async def confirm_delete(facility_to_delete: Dict[str, Any]):
        with ui.dialog() as confirm_dialog, ui.card():
            ui.label(
                f'Are you sure you want to delete facility "{facility_to_delete["name"]}" (ID: {facility_to_delete["id"]})?'
            )
            ui.label(
                "This might also delete associated floors, seats, and assignments!"
            ).classes("text-warning")
            with ui.row():

                async def do_delete():
                    try:
                        await api_client.delete_facility(facility_to_delete["id"])
                        ui.notify(
                            f'Facility "{facility_to_delete["name"]}" deleted.',
                            type="positive",
                        )
                        confirm_dialog.close()
                        await refresh_floors()
                    except Exception as e:
                        ui.notify(f"Error deleting facility: {e}", type="negative")
                        confirm_dialog.close()  # Close even on error

                ui.button("Delete", on_click=do_delete, color="negative")
                ui.button("Cancel", on_click=confirm_dialog.close)
        confirm_dialog.open()

    # --- Initial Data Load ---
    # Use ui.timer for initial load after UI is built
    ui.timer(0.1, refresh_floors, once=True)
