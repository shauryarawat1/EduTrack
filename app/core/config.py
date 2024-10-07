from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduTrack"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_NAME_TEST: str | None = None
    DB_SSLMODE: str = "prefer"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_name = self.DB_NAME_TEST or self.DB_NAME
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{db_name}?sslmode={self.DB_SSLMODE}"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()