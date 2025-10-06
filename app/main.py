from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.api.download import router as download_router
from app.api.quiz import router as quiz_router

app = FastAPI(title="YouTube Key Points Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(routes.router, prefix="/api")
app.include_router(download_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Server running. Open /static/index.html"}
