from typing import Any, List, Dict, Optional, Callable
from nicegui import app  # Use app.storage.user for simple session state

# Store selection globally so right drawer can react
# Use app.storage.user to keep state per browser session


class State:
    # I know...
    def __init__(self):
        self.right_drawer_content_updater = None


STATE = State()


def init_shared_state():
    """Initialize state variables if they don't exist."""
    if "selected_items" not in app.storage.user:
        app.storage.user["selected_items"] = []
    if "selected_item_type" not in app.storage.user:
        app.storage.user["selected_item_type"] = None
    # if "right_drawer_content_updater" not in app.storage.user:
    #     # Placeholder for the function that updates the right drawer
    #     app.storage.user["right_drawer_content_updater"] = None


def set_selected_items(items: List[Dict[str, Any]], item_type: Optional[str]):
    """Update selected items and type, then trigger drawer update."""
    app.storage.user["selected_items"] = items
    app.storage.user["selected_item_type"] = item_type
    # Call the registered updater function if it exists
    updater = (
        STATE.right_drawer_content_updater
    )  # app.storage.user.get("right_drawer_content_updater")
    if callable(updater):
        updater()  # Trigger the update


def get_selected_items() -> List[Dict[str, Any]]:
    return app.storage.user.get("selected_items", [])


def get_selected_item_type() -> Optional[str]:
    return app.storage.user.get("selected_item_type")


def register_right_drawer_updater(func: Callable):
    """Allows the main layout to register the function that rebuilds the drawer."""
    global STATE
    STATE.right_drawer_content_updater = func
    # app.storage.user["right_drawer_content_updater"] = func


def clear_selection():
    """Clears selection and triggers drawer update (to close it)."""
    set_selected_items([], None)
