"""
Human review and workflow model
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Review(Base):
    """Human review decisions"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=False)

    # Reviewer info
    reviewer_id = Column(String(100))
    reviewer_name = Column(String(255))

    # Decision
    decision = Column(String(50))  # approve, reject, flag, investigate
    decision_reason = Column(Text, nullable=True)

    # Feedback for model improvement
    ai_was_correct = Column(Integer, nullable=True)  # 0=no, 1=yes, -1=uncertain
    feedback_notes = Column(Text, nullable=True)

    # Timestamps
    review_timestamp = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    content = relationship("Content", back_populates="reviews")
    analysis = relationship("AnalysisResult", back_populates="reviews")
