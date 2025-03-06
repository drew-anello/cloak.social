from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

# Get the current file's directory and go TWO levels up to find .env in root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

print(f"Looking for .env at: {ENV_PATH}")  # Debug print

# Load the environment variables from the correct path
load_dotenv(ENV_PATH)

# Add error handling for environment variables
PSQLURI = os.getenv('PSQLURI')
PSQLDBNAME = os.getenv('PSQLDBNAME')

if not PSQLURI or not PSQLDBNAME:
    raise ValueError(f"Missing database configuration. Check your .env file at {ENV_PATH}")

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