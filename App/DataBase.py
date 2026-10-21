from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine
from os import getenv
from pathlib import Path
from typing import Generator
from dotenv import load_dotenv

# Prefer a repository/deployment-level .env, while retaining compatibility with
# the existing App/.env location. Existing environment variables always win.
load_dotenv()
load_dotenv(Path(__file__).with_name(".env"))

DB_USER = getenv("DB_USER")

DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")


class ConfigurationError(RuntimeError):
    """Raised when required database configuration is missing or invalid."""


engine = None
SessionLocal = None


def get_database_url():
    """Build the database URL only when configuration is actually needed."""
    database_url = getenv("DATABASE_URL")
    if database_url:
        return database_url

    database_name = getenv("TEST_DB_NAME") or getenv("DB_NAME")
    required_settings = {
        "DB_USER": getenv("DB_USER"),
        "DB_PASS": getenv("DB_PASS"),
        "DB_HOST": getenv("DB_HOST"),
        "DB_PORT": getenv("DB_PORT"),
        "DB_NAME": database_name,
    }
    missing = [name for name, value in required_settings.items() if not value]
    if missing:
        raise ConfigurationError(
            "Missing database configuration: " + ", ".join(missing)
        )

    try:
        port = int(required_settings["DB_PORT"])
    except ValueError as exc:
        raise ConfigurationError("DB_PORT must be an integer") from exc

    return URL.create(
        "mysql+pymysql",
        username=required_settings["DB_USER"],
        password=required_settings["DB_PASS"],
        host=required_settings["DB_HOST"],
        port=port,
        database=database_name,
    )


def validate_database_config():
    get_database_url()


def get_engine():
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(get_database_url())
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine


def dispose_database():
    global engine, SessionLocal
    if engine is not None:
        engine.dispose()
    engine = None
    SessionLocal = None


def get_db() -> Generator[Session, None, None]:
    db = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()
    try:
        yield db
    finally:
        db.close()
        
