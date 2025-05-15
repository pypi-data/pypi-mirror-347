from nicegui import ui

from ..settings import PyFostSettings

settings = PyFostSettings()


def apply_colors(dark=False):
    if dark:
        ui.colors(**settings.colors.dark.model_dump())
    else:
        ui.colors(**settings.colors.light.model_dump())


def dark_mode_switch():
    dark = ui.dark_mode()

    def switch(e):
        dark.toggle()
        apply_colors(dark=dark.value)
        if dark.value:
            e.sender.props("icon=sym_o_light_mode")
        else:
            e.sender.props("icon=sym_o_dark_mode")

    ui.button(icon="sym_o_light_mode", on_click=switch).props("fab")
