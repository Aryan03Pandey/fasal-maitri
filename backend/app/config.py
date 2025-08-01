from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    huggingface_token: str
    gemini_api_key: str
    redis_url: str
    session_ttl: int = 3600
    
    # Neon DB Configuration
    neon_db_url: str
    neon_db_pool_size: int = 10
    neon_db_max_overflow: int = 20
    
    # Twilio Configuration
    twilio_account_sid: str
    twilio_auth_token: str
    whatsapp_from: str
    whatsapp_to: str

    class Config:
        env_file = "../.env"

settings = Settings()
