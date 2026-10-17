from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)

def get_db(): #dependancy injection
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
