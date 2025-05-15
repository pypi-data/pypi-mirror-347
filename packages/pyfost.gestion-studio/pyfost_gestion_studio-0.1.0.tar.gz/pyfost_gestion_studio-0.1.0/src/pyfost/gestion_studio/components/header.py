from nicegui import ui

from .theming import apply_colors, dark_mode_switch


def header(title: str, back_target: str = "/", back_icon: str = "sym_o_home"):
    apply_colors()

    with ui.header(elevated=True):
        with ui.row(align_items="center w-full").classes("xgap-0"):
            if back_target is not None:
                with ui.link(target=back_target):
                    ui.button(icon=back_icon).props("fab").classes("fg-secondary")
            with ui.row(align_items="baseline"):
                ui.image("/assets/fost_studio_logo_noborders.jpeg").classes("w-16")
                ui.label(title).classes("text-h4 text-weight-bolder")
            ui.space()
            dark_mode_switch()
