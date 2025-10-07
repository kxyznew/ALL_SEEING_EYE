#!/usr/bin/env bash
# Simple installer and GUI runner for the YouTube Key Points Summarizer
# Usage:
#   ./install_and_run_gui.sh start   # install deps, start server, open browser
#   ./install_and_run_gui.sh stop    # stop server
#   ./install_and_run_gui.sh status  # show status
#   ./install_and_run_gui.sh restart # restart server

set -Eeuo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${APP_DIR}/.venv"
LOG_DIR="${APP_DIR}/logs"
PID_FILE="${APP_DIR}/.server.pid"
HOST="127.0.0.1"
PORT="${PORT:-8000}"
URL="http://${HOST}:${PORT}/static/index.html"
REQ_FILE="${APP_DIR}/requirements.txt"
UVICORN_APP="app.main:app"

have() { command -v "$1" >/dev/null 2>&1; }

msg() { printf "[%s] %s\n" "$(date +%H:%M:%S)" "$*"; }

install_python_if_needed() {
  if have python3; then return 0; fi
  msg "python3 not found. Attempting to install…"
  if have apt-get; then
    if have sudo; then sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip xdg-utils curl; else apt-get update && apt-get install -y python3 python3-venv python3-pip xdg-utils curl; fi
  elif have dnf; then
    if have sudo; then sudo dnf install -y python3 python3-pip xdg-utils curl; else dnf install -y python3 python3-pip xdg-utils curl; fi
  elif have yum; then
    if have sudo; then sudo yum install -y python3 python3-pip xdg-utils curl; else yum install -y python3 python3-pip xdg-utils curl; fi
  elif have pacman; then
    if have sudo; then sudo pacman -Sy --noconfirm python python-pip xdg-utils curl; else pacman -Sy --noconfirm python python-pip xdg-utils curl; fi
  else
    msg "No supported package manager found. Please install python3 and pip manually."
    return 1
  fi
}

ensure_venv() {
  if [[ -d "${VENV_DIR}" ]]; then return 0; fi
  msg "Creating virtual environment at ${VENV_DIR}"
  if ! have python3; then install_python_if_needed; fi
  python3 -m venv "${VENV_DIR}" || {
    # On Debian/Ubuntu, python3-venv may be missing
    if have apt-get; then
      msg "python3-venv may be missing. Installing…"
      if have sudo; then sudo apt-get install -y python3-venv; else apt-get install -y python3-venv; fi
      python3 -m venv "${VENV_DIR}"
    else
      msg "Failed to create venv. Please ensure python3 venv support is installed."
      return 1
    fi
  }
}

pip_install() {
  msg "Installing Python dependencies"
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
  python -m pip install --upgrade pip wheel
  if [[ -f "${REQ_FILE}" ]]; then
    python -m pip install -r "${REQ_FILE}"
  else
    msg "requirements.txt not found at ${REQ_FILE}"
  fi
}

start_server() {
  mkdir -p "${LOG_DIR}"
  if [[ -f "${PID_FILE}" ]] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
    msg "Server already running with PID $(cat "${PID_FILE}"). Use restart to reload."
    return 0
  fi
  ensure_venv
  pip_install
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
  msg "Starting server on port ${PORT}"
  nohup python -m uvicorn "${UVICORN_APP}" --host 0.0.0.0 --port "${PORT}" --reload >"${LOG_DIR}/server.out" 2>&1 &
  echo $! > "${PID_FILE}"
  # Wait for readiness
  msg "Waiting for server to become ready…"
  for i in {1..60}; do
    if curl -fsS "http://${HOST}:${PORT}/" >/dev/null 2>&1; then
      msg "Server is up. Opening ${URL}"
      if have xdg-open; then xdg-open "${URL}" >/dev/null 2>&1 || true; fi
      if have sensible-browser; then sensible-browser "${URL}" >/dev/null 2>&1 || true; fi
      printf "\nOpen this in your browser: %s\n" "${URL}"
      return 0
    fi
    sleep 0.5
  done
  msg "Server did not become ready in time. Check logs at ${LOG_DIR}/server.out"
}

stop_server() {
  if [[ -f "${PID_FILE}" ]]; then
    local pid
    pid="$(cat "${PID_FILE}")"
    if kill -0 "${pid}" 2>/dev/null; then
      msg "Stopping server PID ${pid}"
      kill "${pid}" || true
      # give it a moment, then force if needed
      sleep 1
      if kill -0 "${pid}" 2>/dev/null; then kill -9 "${pid}" || true; fi
    fi
    rm -f "${PID_FILE}"
  else
    msg "No PID file; server may not be running."
  fi
}

status_server() {
  if [[ -f "${PID_FILE}" ]] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
    msg "Server running (PID $(cat "${PID_FILE}")) at ${URL}"
  else
    msg "Server not running."
  fi
}

case "${1:-start}" in
  start) start_server ;;
  stop) stop_server ;;
  restart) stop_server; start_server ;;
  status) status_server ;;
  *) echo "Usage: $0 {start|stop|restart|status}"; exit 2 ;;
esac
