from pydantic import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # API Keys
    GEMINI_API_KEY: str

    # OAuth
    VK_CLIENT_ID: str
    VK_CLIENT_SECRET: str
    SFERUM_CLIENT_ID: str
    SFERUM_CLIENT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
