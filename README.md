# Python Shark

A simple packet-capture UI built with NiceGUI and scapy.

![Screenshot](image.png)

## Overview

- Live packet capture using scapy running in a background thread.
- NiceGUI frontend shows a compact, searchable table of captured packets.
- Minimal footprint and easy to extend.

## Quick start

1. Create and activate your virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install nicegui scapy pytest
```

3. Run the app from the repository root:

```powershell
python -m app.main
```

Open http://localhost:8080 in your browser.

## Tests

Run the test suite with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Notes

- The UI and CSS assets are in `app/frontend.py` and `app/ui_assets.py`.
- The main server entry is `app/main.py`.
- CI workflow added at `.github/workflows/ci.yml` runs pytest on push/PR.]
