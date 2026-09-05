from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

db_url = "mysql+pymysql://root:Ajoel14%24@localhost:3306/AIresearchHub"
   
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)

def get_db(): #dependancy injection
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
