import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pytest

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_NAME_TEST = os.getenv("DB_NAME_TEST", "edutrack_test")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SSLMODE = os.getenv("DB_SSLMODE")

@pytest.mark.parametrize("db_name", [DB_NAME, DB_NAME_TEST])
def test_connection(db_name):
    db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db_name}?sslmode={DB_SSLMODE}"
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print(f"Connection to {db_name} successful!")
    except Exception as e:
        pytest.fail(f"Connection to {db_name} failed. Error: {e}")

if __name__ == "__main__":
    pytest.main([__file__])