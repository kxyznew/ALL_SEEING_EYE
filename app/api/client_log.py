from fastapi import APIRouter, Request
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ClientLog(BaseModel):
    level: str = "error"
    message: str
    stack: str | None = None
    context: dict | None = None

@router.post("/client-log")
async def client_log(entry: ClientLog, request: Request):
    ip = request.client.host if request.client else "?"
    lvl = entry.level.lower()
    msg = f"[client:{ip}] {entry.message}"
    if entry.stack:
        msg += f"\nSTACK: {entry.stack}"
    if entry.context:
        msg += f"\nCTX: {entry.context}"
    if lvl in ("debug", "info", "warning", "error", "critical"):
        getattr(logger, lvl)(msg)
    else:
        logger.error(msg)
    return {"ok": True}
