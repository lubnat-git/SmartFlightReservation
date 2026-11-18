import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Detect automated testing
TESTING = os.getenv("TESTING", "0").strip() == "1"

# Select the correct database
if TESTING:
    DB_NAME = "flight_system_test"
else:
    DB_NAME = os.getenv("DB_NAME")

# Build database connection
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=3306
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()