#!/usr/bin/env bash
set -euo pipefail
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
