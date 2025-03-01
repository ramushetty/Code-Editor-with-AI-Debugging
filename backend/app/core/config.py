from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://tiger:test_123@localhost/collaborative_code_editor"
    REDIS_URL: str = "redis://localhost:6379"
    FILE_STORAGE_DIR: str = "./file_storage"  # Directory to store code files
    SECRET_KEY: str = "tiger-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GOOGLE_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()