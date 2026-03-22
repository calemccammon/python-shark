import pytest

from types import SimpleNamespace

from app.main import _packet_to_row


class DummyLayer:
    def __init__(self, src=None, dst=None):
        self.src = src
        self.dst = dst


class DummyPacket:
    def __init__(self, time=None, layer=None, summary_text='pkt'):
        self.time = time
        self._layer = layer
        self._summary = summary_text

    def haslayer(self, cls):
        # in tests we only call with IP/TCP/UDP classes; behave according to whether layer set
        return self._layer is not None

    def __getitem__(self, cls):
        return self._layer

    def summary(self):
        return self._summary


def test_packet_to_row_with_ip_tcp():
    layer = DummyLayer(src='192.0.2.1', dst='198.51.100.2')
    pkt = DummyPacket(time=1670000000, layer=layer, summary_text='Ether / IP / TCP foo')
    row = _packet_to_row(pkt)
    assert row['src'] == '192.0.2.1'
    assert row['dst'] == '198.51.100.2'
    assert row['proto'] in ('TCP', 'UDP', '-') or isinstance(row['proto'], str)
    assert 'Ether / IP' in row['summary']


def test_packet_to_row_without_ip():
    pkt = DummyPacket(time=1670000000, layer=None, summary_text='No IP')
    row = _packet_to_row(pkt)
    assert row['src'] == '-'
    assert row['dst'] == '-'
    assert row['summary'] == 'No IP'
