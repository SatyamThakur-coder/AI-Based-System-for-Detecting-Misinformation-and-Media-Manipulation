"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Content schemas
class ContentBase(BaseModel):
    content_type: str
    text_content: Optional[str] = None
    source_url: Optional[str] = None


class ContentCreate(ContentBase):
    pass


class ContentResponse(ContentBase):
    id: int
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    digital_fingerprint: Optional[str] = None
    upload_timestamp: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


# Analysis schemas
class AnalysisResponse(BaseModel):
    id: int
    content_id: int

    # Deepfake detection
    is_deepfake: int
    deepfake_confidence: float
    deepfake_features: Optional[Dict[str, Any]] = None

    # Manipulation
    is_manipulated: int
    manipulation_type: Optional[str] = None
    manipulation_regions: Optional[List[Dict]] = None

    # Fact checking
    fact_check_status: Optional[str] = None
    fact_check_confidence: Optional[float] = None
    claims_extracted: Optional[List[str]] = None
    evidence_sources: Optional[List[Dict]] = None

    # Explanation
    explanation: Optional[str] = None
    features_triggered: Optional[List[str]] = None

    # Assessment
    risk_level: str
    overall_confidence: float

    analysis_timestamp: Optional[datetime] = None
    processing_time_ms: Optional[int] = None

    class Config:
        from_attributes = True


# Review schemas
class ReviewCreate(BaseModel):
    content_id: int
    analysis_id: int
    reviewer_id: str
    reviewer_name: str
    decision: str = Field(..., pattern="^(approve|reject|flag|investigate)$")
    decision_reason: Optional[str] = None
    ai_was_correct: Optional[int] = None
    feedback_notes: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    content_id: int
    analysis_id: int
    reviewer_id: str
    reviewer_name: str
    decision: str
    decision_reason: Optional[str] = None
    review_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True


# Analytics schemas
class AnalyticsOverview(BaseModel):
    total_content_analyzed: int
    misinformation_detected: int
    deepfakes_flagged: int
    accuracy_rate: float
    avg_processing_time_ms: float


class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    avg_latency_ms: float
    human_agreement_rate: float


# Provenance schemas
class ProvenanceCertificate(BaseModel):
    certificate_id: str
    content_id: int
    digital_fingerprint: str
    is_authentic: bool
    confidence: float
    risk_level: str
    issued_at: str
    analysis_summary: Dict[str, Any]
    metadata_integrity: Optional[bool] = None
