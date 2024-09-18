import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import psycopg2

# Load env variables
load_dotenv()

# Retrieve database connection parameters
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SSLMODE = os.getenv("DB_SSLMODE")

# Construct database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"

def print_connection_info():
    print("Database Connection Information:")
    print(f"Username: {DB_USERNAME}")
    print(f"Database: {DB_NAME}")
    print(f"Host: {DB_HOST}")
    print(f"Port: {DB_PORT}")
    print(f"SSL Mode: {DB_SSLMODE}")
    print(f"Connection URL: postgresql://{DB_USERNAME}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}")