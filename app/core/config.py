from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Loads env file

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduTrack"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_SSLMODE: str = "prefer"

