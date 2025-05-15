from nicegui import ui

from ..components.header import header
from ..components.link_lists import big_button_links

from ..settings import PyFostSettings

settings = PyFostSettings()


def home_page():
    header("Gestion Studio", None)
    pages = [
        [
            ("Floor Plans", "sym_o_explore", "apps/floors/"),
            ("Projects", "sym_o_interactive_space", "apps/projects/"),
        ],
        [
            ("Settings", "sym_o_handyman", ""),
            ("API Doc", "auto_fix_high", "/docs"),
        ],
    ]
    big_button_links(pages)
