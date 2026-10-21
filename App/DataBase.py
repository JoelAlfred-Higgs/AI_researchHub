from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL, create_engine
from os import getenv
from pathlib import Path
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


# DATABASE_URL is useful for deployments and lets tests provide an isolated
# database without changing MySQL credentials.  TEST_DB_NAME remains supported
# for the existing MySQL test-database workflow.
DATABASE_NAME = getenv("TEST_DB_NAME") or DB_NAME
db_url = getenv("DATABASE_URL")
if not db_url:
    db_url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=int(DB_PORT) if DB_PORT else None,
        database=DATABASE_NAME,
    )
   
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)

def get_db(): #dependancy injection
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
