from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    PROJECT_NAME: str
    ADMIN_EMAIL: str
    MONGODB_URL: str
    MONGODB_NAME: str
    MONGODB_COLLECTION_PLACES: str
    MONGODB_COLLECTION_USERS: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()