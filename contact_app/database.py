import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DEFAULT_DATABASE_URL = "postgresql+psycopg://appuser:1234@localhost:5559/contactdb"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
engine = None
SessionLocal = None


class Base(DeclarativeBase):
    pass


def configure_database(url: str | None = None) -> None:
    global DATABASE_URL, engine, SessionLocal

    DATABASE_URL = url or os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    engine = create_engine(
        DATABASE_URL,
        future=True,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_db() -> None:
    if engine is None:
        configure_database()
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


configure_database()


def get_db() -> Generator:
    if SessionLocal is None:
        configure_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
