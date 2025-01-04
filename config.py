import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Database engine for PostgreSQL
def get_database_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    return create_engine(DATABASE_URL)
