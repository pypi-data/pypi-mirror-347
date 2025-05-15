from nicegui import ui
from fastapi import APIRouter

# from ....components.theming import apply_colors, dark_mode_switch
from ....components.header import header
from ....components.link_lists import big_button_links
from ...api import FloorsAPI, models

FLOORS_API_CLIENT = None


pages_router = APIRouter()


def project_api() -> FloorsAPI:
    assert FLOORS_API_CLIENT is not None  # Initialized by mount_pages()
    return FLOORS_API_CLIENT


@ui.page(path="/", api_router=pages_router)
def floors_home():
    header("Floor Plans")
    pages = [
        [
            ("Départs/Arrivées", "sym_o_sync_alt", ""),
            ("Stats & Charts", "sym_o_query_stats", ""),
        ],
        [
            ("LBA", "sym_o_map", ""),
            ("LBB", "sym_o_map", ""),
            ("LAA", "sym_o_map", ""),
        ],
        [
            ("Admin", "sym_o_admin_panel_settings", "admin"),
            ("Settings", "sym_o_handyman", ""),
            # ("Users", "sym_o_person_apron", ''),
        ],
    ]
    big_button_links(pages)


def mount_pages(parent_router: APIRouter, api_host: str, api_port: int):
    floors_api = FloorsAPI(host=api_host, port=api_port)
    parent_router.include_router(pages_router)
