from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.api.download import router as download_router
from app.api.quiz import router as quiz_router
from app.api.client_log import router as client_log_router
from app.logging_config import configure_logging
from fastapi import Request
import logging

app = FastAPI(title="YouTube Key Points Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_logging()
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(routes.router, prefix="/api")
app.include_router(download_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")
app.include_router(client_log_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Server running. Open /static/index.html"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"=> {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"<= {request.method} {request.url.path} {response.status_code}")
        return response
    except Exception:
        logger.exception("Unhandled error during request")
        raise
