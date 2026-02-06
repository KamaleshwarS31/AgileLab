from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    openweather_api_key: str
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str
    
    # CORS
    cors_origins: str = "http://localhost:3000"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    
    # Cache
    cache_expiration: int = 300  # 5 minutes
    
    # OpenWeather API
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"
    openweather_onecall_url: str = "https://api.openweathermap.org/data/3.0/onecall"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
