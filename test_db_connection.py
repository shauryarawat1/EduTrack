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
    
# Testing the connection

def test_sqlalchemy_connection():
    print("\nTesting SQLAlchemy connection:")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("SQLAlchemy connection successful!")
    except Exception as e:
        print(f"SQLAlchemy connection failed. Error: {e}")
        
# Testing psycopg2 connection

def test_psycopg2_connection():
    print("\nTesting psycopg2 connection:")
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("psycopg2 connection successful!")
        conn.close()
    except Exception as e:
        print(f"psycopg2 connection failed. Error: {e}")
        
if __name__ == "__main__":
    print_connection_info()
    test_sqlalchemy_connection()
    test_psycopg2_connection()