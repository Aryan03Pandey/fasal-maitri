from pydantic import BaseSettings

class Settings(BaseSettings):
    huggingface_token: str
    gemini_api_key: str
    redis_url: str
    session_ttl: int = 3600

    class Config:
        env_file = "../.env"

settings = Settings()
