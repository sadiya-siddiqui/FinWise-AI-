from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./finwise.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "dev"
    ACCESS_TOKEN_MINUTES: int = 60 * 24
    PLAID_CLIENT_ID: str = ""
    PLAID_SECRET: str = ""
    PLAID_ENV: str = "sandbox"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_MODEL: str = "llama-3.1-70b-versatile"
    CORS_ORIGINS: str = "http://localhost:5173"
    class Config:
        env_file = ".env"

settings = Settings()
