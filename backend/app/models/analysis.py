"""
Analysis results model
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class AnalysisResult(Base):
    """AI analysis results for content"""
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)

    # Deepfake detection
    is_deepfake = Column(Integer, default=0)  # 0=no, 1=yes, -1=uncertain
    deepfake_confidence = Column(Float, default=0.0)  # 0-1
    deepfake_features = Column(JSON, nullable=True)  # Detected features

    # Manipulation detection
    is_manipulated = Column(Integer, default=0)
    manipulation_type = Column(String(100), nullable=True)
    manipulation_regions = Column(JSON, nullable=True)

    # Fact checking
    fact_check_status = Column(String(50), nullable=True)  # True, False, Misleading, Unverified
    fact_check_confidence = Column(Float, nullable=True)
    claims_extracted = Column(JSON, nullable=True)

    # Evidence and sources
    evidence_sources = Column(JSON, nullable=True)
    source_urls = Column(JSON, nullable=True)

    # Explanation
    explanation = Column(Text, nullable=True)
    features_triggered = Column(JSON, nullable=True)

    # Overall assessment
    risk_level = Column(String(50))  # low, medium, high, critical
    overall_confidence = Column(Float, default=0.0)

    # Metadata
    analysis_timestamp = Column(DateTime, server_default=func.now())
    processing_time_ms = Column(Integer, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    content = relationship("Content", back_populates="analyses")
    reviews = relationship("Review", back_populates="analysis", cascade="all, delete-orphan")
