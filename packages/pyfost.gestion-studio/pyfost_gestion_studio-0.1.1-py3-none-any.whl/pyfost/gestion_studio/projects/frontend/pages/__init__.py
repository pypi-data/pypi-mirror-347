from nicegui import ui
from fastapi import APIRouter

from ...api import ProjectsAPI, models
from ....components.header import header

PROJECTS_API_CLIENT = None


pages_router = APIRouter()


def project_api() -> ProjectsAPI:
    assert PROJECTS_API_CLIENT is not None  # Initialized by mount_pages()
    return PROJECTS_API_CLIENT


@ui.page(path="/", api_router=pages_router)
def home():
    header("Projects")
    # apply_colors()
    # with ui.header(elevated=True):
    #     with ui.row(align_items="center w-full"):
    #         with ui.link(target="/"):
    #             ui.button(icon="sym_o_home")
    #         ui.label("Projects").classes("text-lg")
    #         ui.space()
    #         dark_mode_switch()
    #     # with ui.row(align_items="center w-full"):
    #     #     with ui.link(target="/"):
    #     #         ui.button(icon="sym_o_arrow_circle_left")
    #     #     ui.markdown("## Projects")

    with ui.grid(columns=3).classes("gap-2"):
        for i in range(30):
            ui.label(f"Project #{i}").classes("border grow")
            ui.label(f"WIP").classes("border")
            with ui.link(target="admin").classes("border"):
                ui.icon("sym_o_mystery", size="md")  # , color="stone-700")
                # ui.icon("eye")


def mount_pages(parent_router: APIRouter, api_host: str, api_port: int):
    project_api = ProjectsAPI(host=api_host, port=api_port)
    parent_router.include_router(pages_router)
