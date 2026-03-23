"""
Content model for uploaded media
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Content(Base):
    """Uploaded content with metadata"""
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)

    # Content info
    content_type = Column(String(50))  # text, image, video, audio, url
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)

    # Text content
    text_content = Column(Text, nullable=True)

    # URL source
    source_url = Column(String(1000), nullable=True)

    # Metadata
    extended_metadata = Column(JSON, nullable=True)  # EXIF, video metadata, etc.

    # Provenance
    digital_fingerprint = Column(String(64), nullable=True)  # SHA-256 hash
    upload_timestamp = Column(DateTime, server_default=func.now())

    # Processing status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    analyses = relationship("AnalysisResult", back_populates="content", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="content", cascade="all, delete-orphan")
