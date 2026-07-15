import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import database
from .routers import auth, categories, contacts

app = FastAPI(title="Contact Management Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    try:
        database.initialize_db()
    except Exception as exc:  # pragma: no cover - defensive guard for local environments
        logging.getLogger(__name__).warning("Database initialization skipped: %s", exc)

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(categories.router)

static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
