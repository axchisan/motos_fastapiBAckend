from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Taller Mecánico API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URI: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Uploads
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_EXTENSIONS: List[str] = ["png", "jpg", "jpeg", "gif"]
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Stripe
    STRIPE_PUBLIC_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
