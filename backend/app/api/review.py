"""
Review workflow API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Content, AnalysisResult, Review

router = APIRouter(prefix="/api/review", tags=["review"])


@router.get("/queue")
async def get_review_queue(
    risk_level: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Get pending reviews (flagged content)"""
    query = (
        db.query(Content, AnalysisResult)
        .join(AnalysisResult, Content.id == AnalysisResult.content_id)
        .filter(Content.status == "completed")
    )

    if risk_level:
        query = query.filter(AnalysisResult.risk_level == risk_level)

    # Get high-risk or uncertain items for review
    query = query.filter(
        (AnalysisResult.risk_level.in_(["high", "critical"]))
        | (AnalysisResult.overall_confidence < 0.6)
    ).order_by(AnalysisResult.risk_level.desc()).limit(limit)

    results = query.all()

    queue_items = []
    for content, analysis in results:
        existing_review = (
            db.query(Review).filter(Review.content_id == content.id).first()
        )
        queue_items.append({
            "content_id": content.id,
            "content_type": content.content_type,
            "file_name": content.file_name,
            "upload_timestamp": (
                content.upload_timestamp.isoformat() if content.upload_timestamp else None
            ),
            "analysis": {
                "is_deepfake": analysis.is_deepfake,
                "deepfake_confidence": analysis.deepfake_confidence,
                "fact_check_status": analysis.fact_check_status,
                "risk_level": analysis.risk_level,
                "explanation": analysis.explanation,
            },
            "reviewed": existing_review is not None,
            "review_decision": existing_review.decision if existing_review else None,
        })

    return {"total": len(queue_items), "items": queue_items}


@router.post("/{content_id}/approve")
async def approve_analysis(
    content_id: int,
    body: dict = Body(...),
    db: Session = Depends(get_db),
):
    """Approve AI analysis decision"""
    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.content_id == content_id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    review = Review(
        content_id=content_id,
        analysis_id=analysis.id,
        reviewer_id=body.get("reviewer_id", "anonymous"),
        reviewer_name=body.get("reviewer_name", "Human Reviewer"),
        decision="approve",
        ai_was_correct=1,
        feedback_notes=body.get("notes"),
    )
    db.add(review)
    db.commit()
    return {"status": "approved", "content_id": content_id}


@router.post("/{content_id}/reject")
async def reject_analysis(
    content_id: int,
    body: dict = Body(...),
    db: Session = Depends(get_db),
):
    """Reject AI analysis decision"""
    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.content_id == content_id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    review = Review(
        content_id=content_id,
        analysis_id=analysis.id,
        reviewer_id=body.get("reviewer_id", "anonymous"),
        reviewer_name=body.get("reviewer_name", "Human Reviewer"),
        decision="reject",
        decision_reason=body.get("reason", "Rejected by reviewer"),
        ai_was_correct=0,
    )
    db.add(review)
    db.commit()
    return {"status": "rejected", "content_id": content_id}


@router.post("/{content_id}/flag")
async def flag_for_investigation(
    content_id: int,
    body: dict = Body(...),
    db: Session = Depends(get_db),
):
    """Flag content for manual investigation"""
    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.content_id == content_id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    review = Review(
        content_id=content_id,
        analysis_id=analysis.id,
        reviewer_id=body.get("reviewer_id", "anonymous"),
        reviewer_name=body.get("reviewer_name", "Human Reviewer"),
        decision="flag",
        decision_reason=body.get("reason", "Flagged for investigation"),
        ai_was_correct=-1,
    )
    db.add(review)
    db.commit()
    return {"status": "flagged", "content_id": content_id}
