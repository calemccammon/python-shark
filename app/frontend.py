"""Frontend UI builder for the packet-capture app.

This module owns presentation assembly only and returns references
to the few widgets the server needs to update (`stats_label`,
`filter_input`, `packet_table`).
"""

from typing import Tuple, Dict, Any, List, Callable

from nicegui import ui

from app.ui_assets import HEAD_HTML


def build_ui(
    columns: List[Dict[str, Any]],
    rows: List[Dict[str, Any]],
    paused: Dict[str, Any],
    filter_text: Dict[str, Any],
    clear_rows: Callable[[], None],
) -> Tuple[Any, Any, Any]:
    """Construct and return key UI widgets: (stats_label, filter_input, packet_table).

    Keep implementation minimal so tests and maintenance are easier.
    """
    ui.add_head_html(HEAD_HTML)

    with ui.row().classes('controls items-center'):
        stats_label = ui.label('Total packets: 0')
        ui.space()
        ui.label('Filter:')
        filter_input = ui.input('', placeholder='text to filter (src/dst/summary)').style('width:360px; min-width:200px;')

        def apply_filter() -> None:
            filter_text['value'] = (filter_input.value or '').strip().lower()
            try:
                if filter_text['value']:
                    packet_table.rows = [
                        r
                        for r in rows
                        if filter_text['value'] in (r.get('summary', '') or '').lower()
                        or filter_text['value'] in (r.get('src', '') or '').lower()
                        or filter_text['value'] in (r.get('dst', '') or '').lower()
                    ]
                else:
                    packet_table.rows = rows
            except Exception:
                ui.notify('Failed to apply filter', color='negative')

        ui.button('Apply', on_click=apply_filter).classes('q-ml-sm')
        ui.button('Clear Filter', on_click=lambda: (filter_input.set_value(''), apply_filter())).classes('q-ml-sm q-ml-xs')
        ui.button('CLEAR', on_click=lambda: clear_rows()).classes('q-ml-sm')
        ui.switch('Pause updates', value=False, on_change=lambda e: paused.update({'value': e.value})).classes('q-ml-sm')

    with ui.card().classes('table-card shadow-2 q-pa-sm rounded-borders').style('background: var(--card);'):
        ui.label('Captured Packets').classes('text-h6')
        with ui.element('div').style('max-height: calc(100vh - 200px); overflow-y: auto;'):
            packet_table = (
                ui.table(columns=columns, rows=rows, row_key='summary')
                .classes('w-full q-table--bordered q-table--flat compact-table')
            )

    return stats_label, filter_input, packet_table
