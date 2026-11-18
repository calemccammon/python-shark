"""Main application: packet capture + NiceGUI UI startup.

Importing this module starts nothing. `main()` starts the background sniffer
and the server. Presentation is implemented in `app.frontend`.
"""

from collections import deque
from typing import Any
import itertools
import logging
import time
from threading import Lock, Thread

from nicegui import ui
from scapy.all import sniff, Packet
from scapy.layers.inet import IP, TCP, UDP

from app.frontend import build_ui, filter_rows

MAX_ROWS = 5000
SNIFFER_THREAD_NAME = 'packet-sniffer'

# table columns definition for NiceGUI table
columns = [
    {'name': 'time', 'label': 'Time', 'field': 'time', 'style': 'width:90px; text-align:center;'},
    {'name': 'src', 'label': 'Source', 'field': 'src', 'style': 'width:160px;'},
    {'name': 'dst', 'label': 'Destination', 'field': 'dst', 'style': 'width:160px;'},
    {'name': 'proto', 'label': 'Proto', 'field': 'proto', 'style': 'width:90px; text-align:center;'},
    {'name': 'summary', 'label': 'Summary', 'field': 'summary', 'style': 'min-width:360px;'},
]


class PacketStore:
    """Captured rows, newest first, shared by the sniffer thread and every page.

    The store is bounded, so memory stays flat when no page is open or when
    every page is paused. The oldest row is dropped once `max_rows` is reached.
    """

    def __init__(self, max_rows: int) -> None:
        self._rows: deque[dict[str, Any]] = deque(maxlen=max_rows)
        self._lock = Lock()
        self._ids = itertools.count(1)
        self.version = 0

    def add(self, row: dict[str, Any]) -> None:
        """Store a row under a new unique `id`, which the table uses as its row key."""
        with self._lock:
            row['id'] = next(self._ids)
            self._rows.appendleft(row)
            self.version += 1

    def clear(self) -> None:
        with self._lock:
            self._rows.clear()
            self.version += 1

    def snapshot(self) -> tuple[int, list[dict[str, Any]]]:
        """Return the current version and a copy of the rows."""
        with self._lock:
            return self.version, list(self._rows)


store = PacketStore(MAX_ROWS)


def _packet_to_row(pkt: Packet) -> dict[str, Any]:
    """Convert a scapy Packet into a serializable row dict for the table."""
    t_str = time.strftime('%H:%M:%S', time.localtime(float(pkt.time)))
    src = dst = proto = '-'
    if pkt.haslayer(IP):
        ip = pkt[IP]
        src = ip.src or '-'
        dst = ip.dst or '-'
        if pkt.haslayer(TCP):
            proto = 'TCP'
        elif pkt.haslayer(UDP):
            proto = 'UDP'
        else:
            proto = str(ip.proto)
    return {'time': t_str, 'src': src, 'dst': dst, 'proto': proto, 'summary': pkt.summary()}


def packet_callback(packet: Packet) -> None:
    """Callback for scapy.sniff: convert the packet and store the row.

    An exception raised here would end the capture, so a packet that cannot be
    converted is logged and skipped.
    """
    try:
        row = _packet_to_row(packet)
    except Exception:
        logging.exception('Failed converting packet to row')
        return
    store.add(row)


def start_sniffing() -> None:
    """Start sniffing packets using scapy.sniff in the current thread.

    Runs forever (or until the process exits). We start this inside a daemon thread.
    """
    try:
        sniff(prn=packet_callback, store=False)
    except Exception:
        logging.exception('Sniffer failed')


def run_sniffer() -> None:
    """Launch the sniffing thread as a daemon so it doesn't block process exit."""
    t = Thread(target=start_sniffing, name=SNIFFER_THREAD_NAME, daemon=True)
    t.start()


@ui.page('/')
def index() -> None:
    """Build the page for one browser tab and keep its table in step with the store.

    The filter and the pause switch belong to the tab. The captured rows are shared.
    """
    shown = {'filter': '', 'version': -1}

    def refresh() -> None:
        version, rows = store.snapshot()
        packet_table.rows = filter_rows(rows, shown['filter'])
        packet_table.update()
        stats_label.set_text(f'Total packets: {len(rows)}')
        shown['version'] = version

    def apply_filter() -> None:
        shown['filter'] = filter_input.value or ''
        refresh()

    def clear_rows() -> None:
        store.clear()
        filter_input.set_value('')
        apply_filter()

    def on_timer() -> None:
        if not pause_switch.value and store.version != shown['version']:
            refresh()

    with ui.column().classes('min-h-screen'):
        stats_label, filter_input, pause_switch, packet_table = build_ui(
            columns=columns, on_apply=apply_filter, on_clear=clear_rows,
        )
    ui.timer(1.0, on_timer)


def main() -> None:
    """Start the background sniffer and serve the UI."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    run_sniffer()
    ui.run(title='Python Shark', reload=False)


if __name__ == '__main__':
    main()
