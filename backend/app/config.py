"""
Configuration management for AI FactGuard Studio backend
Supports SQLite (default, zero-config) and PostgreSQL (via DATABASE_URL env var)
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    APP_NAME: str = "AI FactGuard Studio"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database — SQLite by default (zero-config), override with PostgreSQL URL
    DATABASE_URL: str = "sqlite:///./factguard.db"

    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "factguard-knowledge"
    NEWSDATA_API_KEY: Optional[str] = None

    # Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB

    # ML Models
    DEEPFAKE_MODEL_PATH: str = "./ml-models/deepfake_detector"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Analysis thresholds
    DEEPFAKE_THRESHOLD: float = 0.7
    FACT_CHECK_CONFIDENCE_THRESHOLD: float = 0.6

    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    @property
    def is_sqlite(self) -> bool:
        """Check if we're using SQLite"""
        return self.DATABASE_URL.startswith("sqlite")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
