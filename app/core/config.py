from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Loads env file

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduTrack"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_SSLMODE: str = "prefer"
    
    @property
    # Constructs database URI
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode={self.DB_SSLMODE}"
    
    class Config:
        env_file = ".env"
        
settings = Settings()