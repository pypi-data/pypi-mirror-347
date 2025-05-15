from typing import TypeVar
from contextlib import asynccontextmanager
from pathlib import Path

from pydantic import BaseModel, IPvAnyNetwork, AnyUrl

from fastapi import FastAPI
from nicegui import ui
from nicegui import app as nicegui_app
import uvicorn

from .. import gestion_studio

from ._version import version

pyfost_getsion_studio_version = version

# --- Settings Models


class AppSettings(BaseModel):
    title: str
    description: str
    version: str = pyfost_getsion_studio_version
    host: IPvAnyNetwork = "127.0.0.1"
    port: int = 8001
    reload: bool = True


class AppBackendSettings(AppSettings):
    database_url: AnyUrl | None = None


class AppFrontendSettings(AppSettings):
    api_host: IPvAnyNetwork = "127.0.0.1"
    api_port: int = 8001
    nice_secret: str = "THIS_IS_NOT_A_SAFE_VALUE"


class AppAllSettings(AppBackendSettings, AppFrontendSettings):
    pass


# --- App Types
AppSettingsType = TypeVar("AppSettingsType")


class _App[AppSettingsType]:
    def __init__(self, settings: AppSettingsType):
        self.settings = settings

    async def startup(self, app: FastAPI) -> None:
        pass

    async def teardown(self, app: FastAPI) -> None:
        pass

    def mount(self, app: FastAPI) -> None:
        pass


class AppBackend(_App[AppBackendSettings]):
    pass


class AppFrontend(_App[AppFrontendSettings]):
    def __init__(self, settings):
        super().__init__(settings)


class AppAll(_App[AppAllSettings]):
    pass


def create_app(
    title,
    description,
    version,
    apps: list[_App],
):
    @asynccontextmanager
    async def lifespan(fastapi_app: FastAPI):
        for app in apps:
            await app.startup(fastapi_app)
        yield
        for app in apps:
            await app.teardown(fastapi_app)

    fastapi_app = FastAPI(
        title=title,
        description=description,
        version=version,
        lifespan=lifespan,
    )

    for app in apps:
        app.mount(fastapi_app)

    from .. import gestion_studio

    assets_path = Path(gestion_studio.__file__) / ".." / "assets"
    assets_path = assets_path.resolve()
    nicegui_app.add_media_files("/assets", assets_path)

    ui.run_with(
        fastapi_app,
        # mount_path=f"/ui",
        title=title,  # Default title for pages without specific one
        storage_secret="storage_secret",  # Needed for session management FIXME: get it from args
        favicon="/assets/favicon/favicon.ico",
    )
    return fastapi_app


def run_app(
    app_object_path: str,
    host: str = "0.0.0.0",
    port: int = 8081,
    reload: bool = True,
):
    uvicorn.run(
        # "pyfost.gestion_studio.projects.backend.main:app",
        app_object_path,
        host=host,
        port=port,
        reload=reload,
    )
