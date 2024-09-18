from sqlalchemy import text
from app.db.base import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful")
            
    except Exception as e:
        print(f"An error has occured: {e}")
        
if __name__ == "__main__":
    test_connection()