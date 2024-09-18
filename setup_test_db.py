import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SSLMODE = os.getenv("DB_SSLMODE")

# Connect to the default 'postgres' database
SQLALCHEMY_DEFAULT_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres?sslmode={DB_SSLMODE}"

engine = create_engine(SQLALCHEMY_DEFAULT_URL)

def setup_test_db():
    db_name = "edutrack_test"
    with engine.connect() as conn:
        # Disable autocommit to run transaction
        conn.execution_options(isolation_level="AUTOCOMMIT")
        try:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created successfully.")
        except ProgrammingError:
            print(f"Database '{db_name}' already exists.")

if __name__ == "__main__":
    setup_test_db()
    print("Test database setup complete.")