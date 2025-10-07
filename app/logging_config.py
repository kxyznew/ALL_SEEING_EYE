import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "errors.log"

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logger = logging.getLogger(record.name)
        if logger.handlers:
            logger.handle(record)

def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    # Rotating file for all logs
    fh = RotatingFileHandler(DEFAULT_LOG_FILE, maxBytes=1_000_000, backupCount=5)
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    # Separate rotating file for errors
    eh = RotatingFileHandler(ERROR_LOG_FILE, maxBytes=1_000_000, backupCount=10)
    eh.setLevel(logging.WARNING)
    eh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    # Reset handlers to avoid duplicates on reload
    root.handlers = []
    root.addHandler(ch)
    root.addHandler(fh)
    root.addHandler(eh)

    # Reduce noise from libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
