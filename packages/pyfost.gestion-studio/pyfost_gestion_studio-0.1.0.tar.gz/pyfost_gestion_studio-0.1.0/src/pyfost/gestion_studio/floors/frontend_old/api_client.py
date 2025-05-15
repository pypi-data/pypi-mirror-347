import httpx
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Union
from datetime import date
import json

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
BASE_URL = BASE_URL if BASE_URL.endswith("/") else BASE_URL + "/"

# Use an async client as NiceGUI runs in asyncio
client = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)


# --- Helper ---
async def _request(method: str, endpoint: str, **kwargs) -> Any:
    """Helper function to make requests and handle basic errors."""
    try:
        response = await client.request(method, endpoint, **kwargs)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        if response.status_code == 204:  # No Content
            return None
        return response.json()
    except httpx.HTTPStatusError as e:
        # Try to get detail from response, otherwise use generic message
        detail = (
            e.response.json().get("detail", e.response.text) if e.response else str(e)
        )
        print(f"HTTP Error: {e.response.status_code} - {detail}")  # Log detailed error
        raise Exception(f"API Error ({e.response.status_code}): {detail}") from e
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
        raise Exception(f"Network or connection error: {e}") from e
    except Exception as e:
        print(f"Unexpected Error during API call: {e}")
        raise Exception("An unexpected error occurred while contacting the API.") from e


# --- API Functions ---


# Facilities
async def get_facilities() -> List[Dict[str, Any]]:
    return await _request("GET", "facilities/")


async def create_facility(name: str) -> Dict[str, Any]:
    return await _request("POST", "facilities/", json={"name": name})


async def delete_facility(facility_id: int) -> None:
    await _request(
        "DELETE", f"facilities/{facility_id}"
    )  # Assuming DELETE returns 204 or similar


# Floors (Example - Adapt for others)
async def get_floors_for_facility(facility_id: int) -> List[Dict[str, Any]]:
    return await _request("GET", f"facilities/{facility_id}/floors/")


async def create_floor(facility_id: int, level: str) -> Dict[str, Any]:
    return await _request(
        "POST", f"facilities/{facility_id}/floors/", json={"level": level}
    )


# Seats
async def get_seats_for_floor(floor_id: int) -> List[Dict[str, Any]]:
    return await _request(
        "GET", f"floors/{floor_id}/seats/?limit=1000"
    )  # Increase limit


async def create_seat(floor_id: int, code: str, x: float, y: float) -> Dict[str, Any]:
    return await _request(
        "POST",
        f"floors/{floor_id}/seats/",
        json={"code": code, "x_coord": x, "y_coord": y},
    )


# Resources
async def get_resources(category: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {"category": category} if category else {}
    return await _request("GET", "resources/", params=params)


async def create_resource(
    identifier: str, category: str, properties: Optional[Dict] = None
) -> Dict[str, Any]:
    payload = {
        "identifier": identifier,
        "resource_category": category,
        "properties": properties or {},
    }
    return await _request("POST", "resources/", json=payload)


async def update_resource(resource_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    # Assuming backend has a PATCH/PUT endpoint for resources
    # Adjust endpoint and method as needed
    return await _request("PATCH", f"resources/{resource_id}", json=data)


async def delete_resource(resource_id: int) -> None:
    await _request("DELETE", f"resources/{resource_id}")


# Assignments
async def get_assignments_for_floor(
    floor_id: int, target_date: date
) -> List[Dict[str, Any]]:
    date_str = target_date.isoformat()
    return await _request("GET", f"floors/{floor_id}/assignments/?date={date_str}")


async def create_assignment(
    seat_id: int, resource_id: int, start_date: date, end_date: date
) -> Dict[str, Any]:
    payload = {
        "seat_id": seat_id,
        "resource_id": resource_id,
        # Ensure dates are sent in 'YYYY-MM-DD' format string
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    return await _request("POST", "assignments/", json=payload)


async def delete_assignment(assignment_id: int) -> None:
    # Assuming a DELETE endpoint exists for assignments
    await _request("DELETE", f"assignments/{assignment_id}")


# Tasks
async def get_tasks(
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    assignee: Optional[str] = None,
) -> List[Dict[str, Any]]:
    params = {}
    if status:
        params["status"] = status
    if task_type:
        params["task_type"] = task_type
    if assignee:
        params["assignee"] = assignee
    return await _request("GET", "tasks/", params=params)


async def update_task(task_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    return await _request("PATCH", f"tasks/{task_id}", json=data)


# Data Management
async def export_data() -> Dict[str, Any]:
    """Gets the data dictionary for export."""
    # Modify API endpoint if it saves file vs returns data
    # Assuming GET /data/export now returns the JSON data directly
    return await _request("GET", "data/export")


async def import_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sends the data dictionary for import."""
    return await _request("POST", "data/import", json=data)


async def import_data_from_file() -> Dict[str, Any]:
    """Triggers the server-side import from file."""
    return await _request("POST", "data/import-from-file")


# Add other API functions (GET specific items, DELETE, PATCH/PUT) as needed...
