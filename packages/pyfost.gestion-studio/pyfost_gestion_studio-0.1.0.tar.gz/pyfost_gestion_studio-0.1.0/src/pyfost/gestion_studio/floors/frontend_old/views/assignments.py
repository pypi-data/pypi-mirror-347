from nicegui import ui, app, events
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

import api_client  # Your API client
from shared_state import set_selected_items  # Import selection handler

# Define columns based on the SeatAssignmentDetail schema from the backend API
columns = [
    # Use assignment_id from the detail schema as the key, but maybe don't display it directly unless needed.
    {
        "name": "assignment_id",
        "label": "ID",
        "field": "assignment_id",
        "sortable": True,
        "align": "left",
        "style": "width: 50px",
    },  # Hidden?
    {
        "name": "seat_code",
        "label": "Seat Code",
        "field": "seat_code",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "resource_identifier",
        "label": "Resource",
        "field": "resource_identifier",
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
    {
        "name": "start_date",
        "label": "Start Date",
        "field": "start_date",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "end_date",
        "label": "End Date",
        "field": "end_date",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "assignment_status",
        "label": "Status",
        "field": "assignment_status",
        "sortable": True,
        "align": "left",
    },
    {"name": "actions", "label": "Actions", "field": "actions", "align": "right"},
]


async def create_ui():
    """Creates the UI for the Assignments view."""
    print("Creating Assignments UI")

    # --- State ---
    assignments: List[Dict[str, Any]] = []
    selected: List[Dict[str, Any]] = []  # Bound to table selection
    pagination = {"page": 1, "rowsPerPage": 15}
    facilities: List[Dict[str, Any]] = []
    floors: List[Dict[str, Any]] = []
    seats: List[Dict[str, Any]] = []  # For Add Dialog
    resources: List[Dict[str, Any]] = []  # For Add Dialog

    # --- Helper Functions ---
    def check_filters() -> bool:
        """Check if all required filters are set."""
        # Ensure elements exist before accessing value
        valid = (
            filter_facility_select
            and filter_facility_select.value
            and filter_floor_select
            and filter_floor_select.value
            and filter_date_input
            and filter_date_input.value
        )
        if not valid:
            ui.notify(
                "Please select a Facility, Floor, and Date first.", type="warning"
            )
        return bool(valid)

    async def load_facilities():
        nonlocal facilities
        # Ensure elements exist before modifying them
        if not filter_facility_select or not add_facility_select:
            print("Warning: Facility select elements not ready during load_facilities.")
            return
        try:
            facilities = await api_client.get_facilities()
            # Set mapping BEFORE assigning options
            filter_facility_select.option_value = "id"
            filter_facility_select.option_label = "name"
            filter_facility_select.options = facilities
            filter_facility_select.update()
            # Also load for add dialog
            add_facility_select.option_value = "id"
            add_facility_select.option_label = "name"
            add_facility_select.options = facilities
            add_facility_select.update()
        except Exception as e:
            ui.notify(f"Error loading facilities: {e}", type="negative")

    async def load_floors(facility_id: int, target_select: ui.select):
        if not target_select:
            print("Warning: Target select element not ready during load_floors.")
            return
        target_select.value = None  # Clear previous selection
        target_select.disable()
        if not facility_id:
            target_select.options = []
            target_select.update()
            return
        try:
            fetched_floors = await api_client.get_floors_for_facility(facility_id)
            # Set mapping BEFORE assigning options
            target_select.option_value = "id"
            target_select.option_label = "level"
            target_select.options = fetched_floors
            target_select.enable()
            target_select.update()
        except Exception as e:
            ui.notify(f"Error loading floors: {e}", type="negative")
            target_select.options = []
            target_select.update()

    async def load_seats_for_add_dialog(floor_id: int):
        nonlocal seats
        if not add_seat_select:
            print(
                "Warning: Add seat select element not ready during load_seats_for_add_dialog."
            )
            return
        add_seat_select.value = None
        add_seat_select.disable()
        if not floor_id:
            add_seat_select.options = []
            seats = []
            add_seat_select.update()
            return
        try:
            fetched_seats = await api_client.get_seats_for_floor(floor_id)
            seats = fetched_seats
            # Transform options AND set mapping explicitly
            transformed_options = [
                {"value": s["id"], "label": s["code"]} for s in fetched_seats
            ]
            add_seat_select.option_value = "value"
            add_seat_select.option_label = "label"
            add_seat_select.options = transformed_options
            add_seat_select.enable()
            add_seat_select.update()
        except Exception as e:
            ui.notify(f"Error loading seats: {e}", type="negative")
            add_seat_select.options = []
            add_seat_select.update()

    async def load_resources_for_add_dialog():
        nonlocal resources
        if not add_resource_select:
            print(
                "Warning: Add resource select element not ready during load_resources_for_add_dialog."
            )
            return
        add_resource_select.disable()
        try:
            fetched_resources = await api_client.get_resources()  # Fetch all for now
            resources = fetched_resources
            # Transform options AND set mapping explicitly
            transformed_options = [
                {"value": r["id"], "label": r["identifier"]} for r in fetched_resources
            ]
            add_resource_select.option_value = "value"
            add_resource_select.option_label = "label"
            add_resource_select.options = transformed_options
            add_resource_select.enable()
            add_resource_select.update()
        except Exception as e:
            ui.notify(f"Error loading resources: {e}", type="negative")
            add_resource_select.options = []
            add_resource_select.update()

    # --- Data Fetching and Refresh Logic ---
    async def refresh_assignments():
        """Fetches assignments based on filters and updates the table."""
        # Ensure table exists before proceeding
        if not table:
            print("Warning: Table not ready for refresh.")
            return

        nonlocal assignments
        if not check_filters():
            assignments[:] = []
            table.rows = assignments
            table.update()
            return

        loading_indicator.visible = True
        table.props("loading=true")
        floor_id = filter_floor_select.value
        target_date_str = filter_date_input.value

        try:
            print(
                f"Refreshing assignments for floor {floor_id} on date {target_date_str}"
            )
            target_date = date.fromisoformat(target_date_str)
            fetched_assignments = await api_client.get_assignments_for_floor(
                floor_id, target_date
            )
            assignments[:] = fetched_assignments
            table.rows = assignments

            selected.clear()
            table.selected.clear()
            set_selected_items([], None)
            table.update()
            print(f"Found {len(assignments)} assignments.")
        except Exception as e:
            ui.notify(
                f"Error fetching assignments: {e}", type="negative", multi_line=True
            )
            assignments[:] = []
            table.rows = assignments
            table.update()
        finally:
            loading_indicator.visible = False
            table.props("loading=false")

    # --- UI Elements ---
    # Define variables for elements before the 'with' block if needed outside immediately
    filter_date_input = None
    filter_facility_select = None
    filter_floor_select = None
    loading_indicator = None
    table = None

    with ui.column().classes("w-full gap-4"):
        # --- Header Row ---
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Manage Assignments").classes("text-h5")
            # Assign to variable defined outside
            loading_indicator = ui.spinner("dots", size="lg", color="primary").props(
                "flat"
            )
            with ui.row().classes("items-center gap-2"):
                ui.button(
                    "Add Assignment", on_click=lambda: add_dialog.open(), icon="add"
                )
                ui.button("Load/Refresh", on_click=refresh_assignments, icon="refresh")

        # --- Filter Row ---
        with ui.row().classes("w-full items-center gap-4"):
            # Assign to variables defined outside
            filter_date_input = (
                ui.date(
                    value=date.today().isoformat(),
                )
                .props('label="Date *" outlined dense stack-label')
                .classes("w-40")
            )

            filter_facility_select = (
                ui.select(options=[], label="Facility *", value=None, with_input=False)
                .props("outlined dense stack-label")
                .classes("w-48")
            )

            filter_floor_select = (
                ui.select(options=[], label="Floor *", value=None, with_input=False)
                .props("outlined dense stack-label")
                .classes("w-40")
                .disable()
            )

        # --- Attach Event Handlers AFTER elements are defined in the layout ---
        # Ensure variables are not None before attaching handlers
        if filter_date_input:
            filter_date_input.on("update:model-value", refresh_assignments)

        async def _handle_facility_change():
            if filter_facility_select:
                fac_id = filter_facility_select.value
                await load_floors(fac_id, filter_floor_select)
                await refresh_assignments()

        if filter_facility_select:
            filter_facility_select.on("update:model-value", _handle_facility_change)

        if filter_floor_select:
            filter_floor_select.on("update:model-value", refresh_assignments)

        # --- Table ---
        # Assign to variable defined outside
        table = (
            ui.table(
                columns=columns,
                rows=[],
                row_key="assignment_id",  # From SeatAssignmentDetail schema
                selection="multiple",
                pagination=pagination,
                on_select=lambda e: set_selected_items(e.selection, "assignment"),
            )
            .classes("w-full")
            .props("dense")
            # .bind_selected(selected)
        )

        # Add action buttons slot
        if table:  # Ensure table exists before adding slots
            table.add_slot(
                "body-cell-actions",
                """
                <q-td :props="props" key="actions" style="width: 1px; padding-right: 16px;">
                    <q-btn flat dense round icon="delete" color="negative" @click="() => $parent.$emit('delete', props.row)"/>
                </q-td>
            """,
            )
            # Handle delete action
            table.on("delete", lambda e: confirm_delete(e.args))
            # Add no-data slot
            with table.add_slot("no-data"):
                ui.label(
                    "Please select a Facility, Floor, and Date to load assignments."
                ).classes("q-pa-md text-grey")

    # --- Dialogs ---
    # Define variables for dialog elements if needed outside immediately
    add_facility_select = None
    add_floor_select = None
    add_seat_select = None
    add_resource_select = None
    add_start_date = None
    add_end_date = None

    with ui.dialog().props("maximized") as add_dialog, ui.card().classes("relative"):
        ui.label("Add New Assignment").classes("text-h6")
        with ui.stepper().props("vertical").classes("w-full") as stepper:
            with ui.step("Location"):
                ui.label("Select the location for the assignment.")
                with ui.row().classes("w-full gap-4"):
                    add_facility_select = (
                        ui.select(options=[], label="Facility *")
                        .props("outlined dense")
                        .classes("flex-1")
                    )
                    add_floor_select = (
                        ui.select(options=[], label="Floor *")
                        .props("outlined dense")
                        .classes("flex-1")
                        .disable()
                    )
                    add_seat_select = (
                        ui.select(options=[], label="Seat *")
                        .props(
                            "outlined dense use-input hide-selected fill-input input-debounce=0"
                        )
                        .classes("flex-1")
                        .disable()
                    )

                # Attach cascading handlers AFTER dialog elements are defined
                async def _add_facility_changed_dialog():
                    if add_facility_select:
                        fac_id = add_facility_select.value
                        await load_floors(fac_id, add_floor_select)
                        if add_seat_select:  # Ensure seat select also exists
                            add_seat_select.value = None
                            add_seat_select.disable()

                async def _add_floor_changed_dialog():
                    if add_floor_select:
                        floor_id = add_floor_select.value
                        await load_seats_for_add_dialog(floor_id)

                if add_facility_select:
                    add_facility_select.on(
                        "update:model-value", _add_facility_changed_dialog
                    )
                if add_floor_select:
                    add_floor_select.on("update:model-value", _add_floor_changed_dialog)

                with ui.stepper_navigation():
                    ui.button("Next", on_click=stepper.next).props("color=primary")

            with ui.step("Resource"):
                ui.label("Select the resource to assign.")
                add_resource_select = (
                    ui.select(options=[], label="Resource *")
                    .props(
                        "outlined dense use-input hide-selected fill-input input-debounce=0"
                    )
                    .classes("w-full")
                    .disable()
                )

                with ui.stepper_navigation():
                    ui.button("Next", on_click=stepper.next).props("color=primary")
                    ui.button("Back", on_click=stepper.previous).props("flat")

            with ui.step("Period"):
                ui.label("Select the start and end dates for the assignment.")
                with ui.row().classes("w-full gap-4"):
                    add_start_date = (
                        ui.date()
                        .props('label="Start Date *" outlined dense stack-label')
                        .classes("flex-1")
                    )
                    add_end_date = (
                        ui.date()
                        .props('label="End Date *" outlined dense stack-label')
                        .classes("flex-1")
                    )

                with ui.stepper_navigation():
                    ui.button(
                        "Create Assignment", on_click=lambda: handle_add_assignment()
                    )
                    ui.button("Back", on_click=stepper.previous).props("flat")

        # --- Add Dialog Logic (handle_add_assignment remains the same) ---
        async def handle_add_assignment():
            # Ensure elements exist before accessing value
            seat_id = add_seat_select.value if add_seat_select else None
            resource_id = add_resource_select.value if add_resource_select else None
            start_date_str = add_start_date.value if add_start_date else None
            end_date_str = add_end_date.value if add_end_date else None

            errors = []
            if not seat_id:
                errors.append("Seat is required.")
            if not resource_id:
                errors.append("Resource is required.")
            if not start_date_str:
                errors.append("Start Date is required.")
            if not end_date_str:
                errors.append("End Date is required.")

            start_d, end_d = None, None
            try:  # Add try-except for date parsing
                if start_date_str:
                    start_d = date.fromisoformat(start_date_str)
                if end_date_str:
                    end_d = date.fromisoformat(end_date_str)
            except ValueError:
                errors.append("Invalid date format.")

            if start_d and end_d and end_d < start_d:
                errors.append("End date cannot be before start date.")

            if errors:
                ui.notify(". ".join(errors), type="warning", multi_line=True)
                return

            try:
                await api_client.create_assignment(
                    seat_id=seat_id,
                    resource_id=resource_id,
                    start_date=start_d,
                    end_date=end_d,
                )
                ui.notify(
                    "Assignment created successfully! Tasks are generated in the background.",
                    type="positive",
                )
                add_dialog.close()

                current_filter_date = (
                    date.fromisoformat(filter_date_input.value)
                    if filter_date_input and filter_date_input.value
                    else None
                )
                if current_filter_date and start_d <= current_filter_date <= end_d:
                    await refresh_assignments()
                else:
                    ui.notify(
                        "Assignment created but is outside the current filter date.",
                        type="info",
                    )

            except Exception as e:
                ui.notify(
                    f"Error creating assignment: {e}", type="negative", multi_line=True
                )

        # Cancel button
        ui.button("Cancel", on_click=add_dialog.close).props("flat color=grey").classes(
            "absolute-top-right q-mr-md q-mt-sm"
        )

        # Load initial data for dialog selectors when it opens
        add_dialog.on("before_show", load_resources_for_add_dialog)
        add_dialog.on("before_show", load_facilities)

    # --- Delete Confirmation Dialog (confirm_delete remains the same) ---
    async def confirm_delete(assignment_to_delete: Dict[str, Any]):
        # Ensure assignment_id exists in the data passed from the table
        assignment_id = assignment_to_delete.get("assignment_id")
        if assignment_id is None:
            ui.notify(
                "Cannot delete: Assignment ID missing from row data.", type="negative"
            )
            return

        with ui.dialog() as confirm_dialog, ui.card():
            ui.label(f"Delete Assignment?").classes("text-h6")
            ui.label(
                f'Are you sure you want to delete the assignment for resource "{assignment_to_delete.get("resource_identifier", "N/A")}" at seat "{assignment_to_delete.get("seat_code", "N/A")}" (ID: {assignment_id})?'
            )
            ui.label("This will also delete associated pending tasks!").classes(
                "text-warning"
            )
            with ui.row().classes("justify-end w-full"):

                async def do_delete():
                    try:
                        await api_client.delete_assignment(assignment_id)
                        ui.notify(f"Assignment deleted.", type="positive")
                        confirm_dialog.close()
                        await refresh_assignments()  # Refresh the current view
                    except Exception as e:
                        ui.notify(
                            f"Error deleting assignment: {e}",
                            type="negative",
                            multi_line=True,
                        )
                        confirm_dialog.close()

                ui.button("Delete", on_click=do_delete, color="negative")
                ui.button("Cancel", on_click=confirm_dialog.close)
        confirm_dialog.open()

    # --- Initial Data Load ---
    # Load facilities immediately for the filter dropdown
    await load_facilities()
    # The 'no-data' slot in the table definition handles the initial message.
