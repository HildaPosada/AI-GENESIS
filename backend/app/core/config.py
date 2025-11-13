"""
Configuration management for AI Fraud Detection System
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # App Settings
    APP_NAME: str = "AI Fraud Detection System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API Keys - All 4 Hackathon Technologies
    GOOGLE_API_KEY: Optional[str] = None  # Google Gemini
    OPUS_API_KEY: Optional[str] = None     # Opus Workflow Automation
    AIML_API_KEY: Optional[str] = None     # AI/ML API
    ANTHROPIC_API_KEY: Optional[str] = None  # For Claude via AI/ML API
    OPENAI_API_KEY: Optional[str] = None   # For GPT via AI/ML API

    # Qdrant Vector Database
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "fraud_patterns"
    QDRANT_API_KEY: Optional[str] = None

    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Database
    DATABASE_URL: str = "sqlite:///./fraud_detection.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ML Models
    FRAUD_THRESHOLD: float = 0.75
    ANOMALY_THRESHOLD: float = 0.85

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
