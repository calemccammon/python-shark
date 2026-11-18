"""Frontend UI builder for the packet-capture app.

This module owns presentation assembly only and returns references
to the few widgets the server needs to read or update (`stats_label`,
`filter_input`, `pause_switch`, `packet_table`).
"""

from typing import Any, Callable

from nicegui import ui

from app.ui_assets import HEAD_HTML

FILTER_FIELDS = ('src', 'dst', 'summary')


def filter_rows(rows: list[dict[str, Any]], text: str) -> list[dict[str, Any]]:
    """Return the rows whose source, destination or summary contains `text`.

    The match is a case-insensitive substring match. Blank text matches every row.
    """
    needle = text.strip().lower()
    if not needle:
        return list(rows)
    return [r for r in rows if any(needle in r[field].lower() for field in FILTER_FIELDS)]


def build_ui(
    columns: list[dict[str, Any]],
    on_apply: Callable[[], None],
    on_clear: Callable[[], None],
) -> tuple[Any, Any, Any, Any]:
    """Construct and return key UI widgets: (stats_label, filter_input, pause_switch, packet_table).

    `on_apply` is called when the filter should be re-read from `filter_input`.
    `on_clear` is called by the CLEAR button.
    """
    ui.add_head_html(HEAD_HTML)

    with ui.row().classes('controls items-center'):
        stats_label = ui.label('Total packets: 0')
        ui.space()
        ui.label('Filter:')
        filter_input = ui.input('', placeholder='text to filter (src/dst/summary)').style('width:360px; min-width:200px;')

        ui.button('Apply', on_click=on_apply).classes('q-ml-sm')
        ui.button('Clear Filter', on_click=lambda: (filter_input.set_value(''), on_apply())).classes('q-ml-sm q-ml-xs')
        ui.button('CLEAR', on_click=on_clear).classes('q-ml-sm')
        pause_switch = ui.switch('Pause updates', value=False).classes('q-ml-sm')

    with ui.card().classes('table-card shadow-2 q-pa-sm rounded-borders').style('background: var(--card);'):
        ui.label('Captured Packets').classes('text-h6')
        with ui.element('div').style('max-height: calc(100vh - 200px); overflow-y: auto;'):
            packet_table = (
                ui.table(columns=columns, rows=[], row_key='id')
                .classes('w-full q-table--bordered q-table--flat compact-table')
            )

    return stats_label, filter_input, pause_switch, packet_table
