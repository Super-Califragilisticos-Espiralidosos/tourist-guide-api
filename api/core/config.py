from pydantic import BaseSettings
from secrets import token_urlsafe

class Settings(BaseSettings):
    SECRET_KEY: str = token_urlsafe(32)
    PROJECT_NAME: str
    ADMIN_EMAIL: str
    MONGODB_URL: str
    MONGODB_NAME: str
    MONGODB_COLLECTION_PLACES: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()