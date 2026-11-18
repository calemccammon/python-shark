import threading
import time

from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.packet import Raw

from app.frontend import filter_rows
from app.main import SNIFFER_THREAD_NAME, PacketStore, _packet_to_row

SRC = '192.0.2.1'
DST = '198.51.100.2'
TIMESTAMP = 1670000000


def _row(src='10.0.0.1', dst='10.0.0.2', summary='IP / TCP'):
    return {'time': '00:00:00', 'src': src, 'dst': dst, 'proto': 'TCP', 'summary': summary}


def test_importing_main_does_not_start_the_sniffer():
    assert all(t.name != SNIFFER_THREAD_NAME for t in threading.enumerate())


def test_packet_to_row_tcp():
    pkt = IP(src=SRC, dst=DST) / TCP()
    pkt.time = TIMESTAMP
    row = _packet_to_row(pkt)
    assert row == {
        'time': time.strftime('%H:%M:%S', time.localtime(TIMESTAMP)),
        'src': SRC,
        'dst': DST,
        'proto': 'TCP',
        'summary': pkt.summary(),
    }


def test_packet_to_row_udp():
    row = _packet_to_row(IP(src=SRC, dst=DST) / UDP())
    assert row['proto'] == 'UDP'
    assert row['src'] == SRC
    assert row['dst'] == DST


def test_packet_to_row_other_ip_protocol_shows_its_number():
    # Parse the packet from bytes, as a captured packet would be.
    pkt = IP(bytes(IP(src=SRC, dst=DST) / ICMP()))
    row = _packet_to_row(pkt)
    assert row['proto'] == '1'
    assert row['src'] == SRC
    assert row['dst'] == DST


def test_packet_to_row_without_ip():
    pkt = Raw(load=b'hello')
    row = _packet_to_row(pkt)
    assert row['src'] == '-'
    assert row['dst'] == '-'
    assert row['proto'] == '-'
    assert row['summary'] == pkt.summary()


def test_store_returns_newest_first_with_unique_ids():
    store = PacketStore(max_rows=10)
    store.add(_row(summary='same'))
    store.add(_row(summary='same'))
    _, rows = store.snapshot()
    assert len(rows) == 2
    assert rows[0]['id'] > rows[1]['id']


def test_store_drops_oldest_rows_beyond_max():
    store = PacketStore(max_rows=3)
    for i in range(5):
        store.add(_row(summary=str(i)))
    _, rows = store.snapshot()
    assert [r['summary'] for r in rows] == ['4', '3', '2']


def test_store_version_changes_on_add_and_clear():
    store = PacketStore(max_rows=3)
    v0, _ = store.snapshot()
    store.add(_row())
    v1, _ = store.snapshot()
    store.clear()
    v2, rows = store.snapshot()
    assert v0 != v1 != v2
    assert rows == []


def test_filter_rows_matches_src_dst_and_summary_case_insensitively():
    rows = [
        _row(src='192.0.2.1', dst='10.0.0.9', summary='IP / TCP'),
        _row(src='10.0.0.5', dst='198.51.100.2', summary='IP / UDP / DNS Qry'),
        _row(src='10.0.0.6', dst='10.0.0.7', summary='IP / ICMP'),
    ]
    assert filter_rows(rows, '192.0.2') == [rows[0]]
    assert filter_rows(rows, '198.51') == [rows[1]]
    assert filter_rows(rows, ' dns ') == [rows[1]]
    assert filter_rows(rows, 'no such text') == []


def test_filter_rows_blank_text_returns_all_rows():
    rows = [_row(), _row()]
    assert filter_rows(rows, '   ') == rows
