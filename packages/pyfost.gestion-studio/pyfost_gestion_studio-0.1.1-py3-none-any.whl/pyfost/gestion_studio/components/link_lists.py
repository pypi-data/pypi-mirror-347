from nicegui import ui


def big_button_links(pages: list[list[tuple[str, str, str]]]):
    """
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
    """
    with ui.column(align_items="center").classes("p-8 w-full bg-box1"):
        for pages_group in pages:
            with ui.row().classes("bg-box2"):
                for title, icon, target in pages_group:
                    with ui.card().classes("gap-0"):
                        with ui.row().classes("w-full"):
                            ui.space()
                            with ui.link(target=target).classes("!no-underline"):
                                with ui.column(align_items="center"):
                                    ui.icon(icon, size="xl", color="primary")
                                    ui.label(title).classes("text-lg text-secondary")
                            ui.space()
