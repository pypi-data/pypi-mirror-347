# framework/ui_components.py
from typing import List, Dict, Callable, Any, Optional, Type
from nicegui import ui
from pydantic import BaseModel


# --- Entity Table Component ---
def entity_table(
    *,
    columns: List[Dict[str, Any]],  # NiceGUI table column definition
    rows: List[Dict[str, Any]],  # Data rows
    id_field: str,  # Name of the ID field
    on_create: Callable[[], None],  # Callback when 'Create' is clicked
    on_edit: Callable[[Any], None],  # Callback when 'Edit' is clicked (passes ID)
    on_delete: Callable[[Any], None],  # Callback when 'Delete' is clicked (passes ID)
) -> None:
    """
    Renders a table for displaying entities with Create, Edit, Delete actions.

    Args:
        columns: List of column definitions for ui.table.
        rows: List of data dictionaries for the table rows.
        id_field: The key in the row dictionary representing the unique ID.
        on_create: Function to call when the 'Create New' button is clicked.
        on_edit: Function to call when an 'Edit' button is clicked.
        on_delete: Function to call when a 'Delete' button is clicked.
    """
    with ui.row().classes("w-full items-center"):
        ui.button("Create New", on_click=on_create, icon="add")
        # Add search/filter later if needed
        ui.space()

    action_column = {
        "name": "actions",
        "label": "Actions",
        "sortable": False,
        "align": "right",
    }

    # Ensure ID field is present for actions, even if not displayed explicitly
    all_column_names = [col["name"] for col in columns]
    if id_field not in all_column_names:
        columns.append(
            {
                "name": id_field,
                "label": "ID",
                "field": id_field,
                "required": True,
                "align": "left",
                "sortable": True,
                "style": "display: none",
            }
        )  # Hide if not needed for display

    table = ui.table(
        columns=[*columns, action_column], rows=rows, row_key=id_field
    ).classes("w-full")

    # Define slots for actions (buttons in the action column)
    table.add_slot(
        f"body-cell-actions",
        """
        <q-td :props="props" key="actions">
            <q-btn flat dense round @click="$parent.$emit('edit', props.row); console.log('?')" icon="edit" />
            <q-btn flat dense round @click="$parent.$emit('delete', props.row)" icon="delete" color="red-7"/>
        </q-td>
    """,
    )

    # Connect table events to callbacks
    table.on("edit", lambda e: on_edit(e.args[id_field]))
    table.on("delete", lambda e: on_delete(e.args[id_field]))


# --- Entity Form Component ---
def entity_form(
    *,
    model: Type[BaseModel],  # Pydantic model for schema reference
    id_field: str,  # Name of the ID field
    initial_data: Optional[
        Dict[str, Any]
    ] = None,  # Data for editing, None for creating
    on_save: Callable[[Dict[str, Any]], None],  # Callback on save (passes form data)
    on_cancel: Callable[[], None],  # Callback on cancel
) -> None:
    """
    Renders a form based on a Pydantic model for creating or editing an entity.

    Args:
        model: The Pydantic model defining the fields.
        id_field: The name of the ID field (used to disable/hide it).
        initial_data: Existing data to populate the form for editing.
        on_save: Function to call with the form data when 'Save' is clicked.
        on_cancel: Function to call when 'Cancel' is clicked.
    """
    is_edit_mode = initial_data is not None
    form_data = initial_data.copy() if is_edit_mode else {}
    form_elements: Dict[str, ui.element] = {}

    # Dynamically create form fields based on the Pydantic model
    schema = model.model_json_schema()
    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])

    with ui.card().classes("w-full"):  # Use card for better visual grouping
        for name, props in properties.items():
            if name == id_field:  # Never edit the ID field directly in the form
                if is_edit_mode:
                    # Display ID for context but disable it
                    ui.input(
                        label=f"{props.get('title', name)} (ID)",
                        value=initial_data.get(name),
                    ).props("readonly disable")
                continue  # Don't create editable input for ID

            label = props.get("title", name).replace("_", " ").title()
            field_type = props.get("type")
            is_required = name in required_fields
            current_value = (
                initial_data.get(name) if is_edit_mode else props.get("default")
            )

            element = None
            validation = (
                {"required": lambda v: v is not None and v != ""} if is_required else {}
            )

            # Basic type mapping (can be expanded)
            if "enum" in props:
                element = ui.select(
                    props["enum"], label=label, value=current_value
                ).props("emit-value map-options")
            elif field_type == "string":
                # Could check props.get('format') for 'date-time', 'email', etc.
                element = ui.input(
                    label=label, value=current_value, validation=validation
                )
            elif field_type == "boolean":
                element = ui.switch(
                    label, value=current_value
                )  # Use switch instead of checkbox
            elif field_type == "integer":
                element = ui.number(
                    label=label,
                    value=current_value,
                    format="%.0f",
                    validation=validation,
                )
            elif field_type == "number":  # Includes float
                element = ui.number(
                    label=label, value=current_value, validation=validation
                )
            # Add more type handlers (UUID, relationships potentially as selects) here later
            else:
                # Fallback for unsupported types
                element = ui.input(
                    label=f"{label} (Unsupported Type: {field_type})",
                    value=str(current_value),
                ).props("disable")

            if element:
                form_elements[name] = element
                # Bind input changes back to our form_data dictionary
                # Note: ui.switch provides 'value' not 'text' or 'number-value'
                if isinstance(element, ui.switch):
                    element.bind_value(form_data, name)
                elif isinstance(element, (ui.input, ui.textarea, ui.select)):
                    element.bind_value(form_data, name)
                elif isinstance(element, ui.number):
                    element.bind_value(
                        form_data, name
                    )  # NiceGUI handles number binding

        # --- Form Actions ---
        with ui.row().classes("w-full justify-end q-mt-md"):
            ui.button("Cancel", on_click=on_cancel, color="grey")
            ui.button("Save", on_click=lambda: on_save(form_data))


# --- Confirmation Dialog ---
async def show_confirmation_dialog(
    title: str, message: str, confirm_text: str = "Confirm", cancel_text: str = "Cancel"
) -> bool:
    """Shows a modal confirmation dialog and returns True if confirmed, False otherwise."""
    result = None
    with ui.dialog() as dialog, ui.card():
        ui.label(title).classes("text-h6")
        ui.label(message).classes("q-my-md")
        with ui.row().classes("w-full justify-end"):
            ui.button(cancel_text, on_click=lambda: dialog.submit(False), color="grey")
            ui.button(confirm_text, on_click=lambda: dialog.submit(True))

    result = await dialog
    return result if result is not None else False
