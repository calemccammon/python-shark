"""Main application: packet capture + NiceGUI UI startup.

Keep this file minimal: start background sniffer, wire UI, and run server.
Presentation is implemented in `app.frontend`.
"""

from typing import Dict, List, Any
import logging
import time
from threading import Thread
import queue

from nicegui import ui
from scapy.all import sniff, Packet
from scapy.layers.inet import IP, TCP, UDP

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Thread-safe queue for packets
data_queue: queue.Queue[Packet] = queue.Queue()

# Packet capture callback
def packet_callback(packet: Packet) -> None:
    """Callback for scapy.sniff: enqueue received packets for UI processing.

    Separated from UI to keep capture concerns isolated from presentation.
    """
    try:
        data_queue.put(packet)
    except Exception:
        logging.exception('Failed to queue packet')

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
    t = Thread(target=start_sniffing, daemon=True)
    t.start()

# table columns definition for NiceGUI table
columns = [
    {'name': 'time', 'label': 'Time', 'field': 'time', 'style': 'width:90px; text-align:center;'},
    {'name': 'src', 'label': 'Source', 'field': 'src', 'style': 'width:160px;'},
    {'name': 'dst', 'label': 'Destination', 'field': 'dst', 'style': 'width:160px;'},
    {'name': 'proto', 'label': 'Proto', 'field': 'proto', 'style': 'width:90px; text-align:center;'},
    {'name': 'summary', 'label': 'Summary', 'field': 'summary', 'style': 'min-width:360px;'},
]

# Application state
rows: List[Dict[str, Any]] = []
paused = {'value': False}
MAX_ROWS = 5000
filter_text = {'value': ''}
def clear_rows() -> None:
    """Clear stored rows and drain the packet queue."""
    rows.clear()
    # drain queue
    try:
        while True:
            data_queue.get_nowait()
    except queue.Empty:
        pass
    # update UI elements if present
    try:
        filter_input.set_value('')
    except Exception:
        logging.debug('filter_input not available to clear')
    filter_text['value'] = ''
    try:
        packet_table.rows = []
    except Exception:
        logging.debug('packet_table not initialized')
    try:
        stats_label.set_text(f'Total packets: {len(rows)}')
    except Exception:
        logging.debug('stats_label not initialized')

from app.frontend import build_ui


with ui.column().classes('min-h-screen'):
    stats_label, filter_input, packet_table = build_ui(columns=columns, rows=rows, paused=paused, filter_text=filter_text, clear_rows=clear_rows)

# periodic update
def _packet_to_row(pkt: Packet) -> Dict[str, str]:
    """Convert a scapy Packet into a serializable row dict for the table."""
    t = getattr(pkt, 'time', time.time())
    t_str = time.strftime('%H:%M:%S', time.localtime(t))
    src = dst = proto = '-'
    try:
        if pkt.haslayer(IP):
            ip = pkt[IP]
            src = getattr(ip, 'src', '-') or '-'
            dst = getattr(ip, 'dst', '-') or '-'
            if pkt.haslayer(TCP):
                proto = 'TCP'
            elif pkt.haslayer(UDP):
                proto = 'UDP'
            else:
                proto = str(getattr(ip, 'proto', '-'))
    except Exception:
        logging.debug('Failed to extract IP/TCP/UDP from packet', exc_info=True)
    summary = pkt.summary() if hasattr(pkt, 'summary') else str(pkt)
    return {'time': t_str, 'src': src, 'dst': dst, 'proto': proto, 'summary': summary}


def update_table() -> None:
    """Timer callback: drain queued packets, update rows and the NiceGUI table.

    This keeps UI updates on the main thread while capture runs in background.
    """
    if paused.get('value'):
        return
    updated = False
    # drain the queue
    while True:
        try:
            pkt = data_queue.get_nowait()
        except queue.Empty:
            break
        try:
            row = _packet_to_row(pkt)
            rows.insert(0, row)  # newest first
            updated = True
        except Exception:
            logging.exception('Failed converting packet to row')

    # trim to MAX_ROWS
    if len(rows) > MAX_ROWS:
        del rows[MAX_ROWS:]

    if updated:
        filt = (filter_text.get('value') or '').strip().lower()
        try:
            if filt:
                packet_table.rows = [r for r in rows if filt in (r.get('summary', '') or '').lower() or filt in (r.get('src', '') or '').lower() or filt in (r.get('dst', '') or '').lower()]
            else:
                packet_table.rows = rows
        except Exception:
            logging.exception('Failed updating packet_table.rows')
        try:
            stats_label.set_text(f'Total packets: {len(rows)}')
        except Exception:
            logging.debug('Failed updating stats_label')

# Start background sniffer and UI timer (UI constructed above via frontend.build_ui)
run_sniffer()
ui.timer(1.0, update_table)


if __name__ == '__main__':
    ui.run(title='Python Shark', reload=False)
