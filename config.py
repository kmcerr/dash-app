import os
from dotenv import load_dotenv
from pyngrok import ngrok
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Environment Variables
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize ngrok
def init_ngrok(port=8055):
    """
    Initialize ngrok to create a public URL for the Dash app.
    """
    if NGROK_AUTH_TOKEN:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(port).public_url
    print(f"ngrok tunnel available at: {public_url}")
    return public_url

# Database Engine
def get_database_engine():
    """
    Create and return a SQLAlchemy engine for PostgreSQL.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    return create_engine(DATABASE_URL)
