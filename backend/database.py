from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Add error handling for environment variables
PSQLURI = os.getenv('PSQLURI')
PSQLDBNAME = os.getenv('PSQLDBNAME')

if not PSQLURI or not PSQLDBNAME:
    raise ValueError("Missing database configuration. Check your .env file.")

PSQLURL = f"{PSQLURI}{PSQLDBNAME}"
print(f"Connecting to database: {PSQLURL}")  # Debug print

engine = create_engine(PSQLURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()