# Python Shark

A simple packet-capture UI built with NiceGUI and scapy.

![Screenshot](image.png)

## Overview

- Live packet capture using scapy running in a background thread.
- NiceGUI frontend shows a compact table of captured packets, newest first, with time, source, destination, protocol and scapy's summary line.
- A text filter matches on source, destination or summary. A switch pauses table updates, and a button clears the captured rows.

## Quick start

Requires Python 3.11 or newer.

1. Create and activate a virtual environment.

   Bash (Linux, macOS):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project and its dev dependencies as an editable install:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   ```

3. Run the app from the repository root:

   ```bash
   python -m app.main
   ```

Open http://localhost:8080 in your browser.

Packet capture usually needs elevated privileges: root or the `CAP_NET_RAW` capability on Linux, and Npcap on Windows. Without them the sniffer thread logs `Sniffer failed` and the table stays empty.

## How it works

`app/main.py` starts `scapy.sniff` in a daemon thread. The callback puts each packet on a queue. A NiceGUI timer drains the queue once a second, converts each packet to a row and updates the table, so the UI is only touched from the NiceGUI event loop. The table keeps the most recent 5000 rows.

- `app/main.py`: capture thread, row conversion, timer and server entry point
- `app/frontend.py`: page layout and filter controls
- `app/ui_assets.py`: CSS and the light/dark theme script

## Tests

Run the test suite (from the repo root):

```bash
python -m pytest -q
```

There are two tests, both for the packet-to-row conversion. The CI workflow at `.github/workflows/ci.yml` runs pytest on push and pull request.

## Limitations

- The Proto column names only TCP and UDP. Other IPv4 packets show the IP protocol number, and non-IPv4 packets such as ARP and IPv6 show `-` for source, destination and protocol.
- Pausing stops table updates, not capture. Packets keep queueing in memory until updates resume.
- There is no interface selection or capture filter. scapy sniffs on its default interface.
