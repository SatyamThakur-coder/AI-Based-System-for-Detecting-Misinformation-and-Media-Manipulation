"""
Analytics and metrics API endpoints
SQLite-compatible date functions + demo data seeding
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import random
from app.db.database import get_db
from app.models import Content, AnalysisResult, Review
from app.config import settings

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview", response_model=dict)
async def get_overview(db: Session = Depends(get_db)):
    """Get dashboard overview metrics"""

    total_content = (
        db.query(func.count(Content.id))
        .filter(Content.status == "completed")
        .scalar()
        or 0
    )

    misinformation = (
        db.query(func.count(AnalysisResult.id))
        .filter(
            (AnalysisResult.fact_check_status.in_(["False", "Misleading"]))
            | (AnalysisResult.is_deepfake == 1)
        )
        .scalar()
        or 0
    )

    deepfakes = (
        db.query(func.count(AnalysisResult.id))
        .filter(AnalysisResult.is_deepfake == 1)
        .scalar()
        or 0
    )

    total_reviews = db.query(func.count(Review.id)).scalar() or 0
    correct_predictions = (
        db.query(func.count(Review.id))
        .filter(Review.ai_was_correct == 1)
        .scalar()
        or 0
    )

    accuracy_rate = (correct_predictions / total_reviews * 100) if total_reviews > 0 else 0.0

    avg_processing_time = (
        db.query(func.avg(AnalysisResult.processing_time_ms)).scalar() or 0.0
    )

    return {
        "total_content_analyzed": total_content,
        "misinformation_detected": misinformation,
        "deepfakes_flagged": deepfakes,
        "accuracy_rate": round(accuracy_rate, 2),
        "avg_processing_time_ms": round(float(avg_processing_time), 2),
        "total_reviews": total_reviews,
    }


@router.get("/metrics", response_model=dict)
async def get_metrics(db: Session = Depends(get_db)):
    """Get detailed performance metrics — works even without reviews"""

    # Average latency from ALL analysis results (doesn't need reviews)
    avg_latency = (
        db.query(func.avg(AnalysisResult.processing_time_ms))
        .filter(AnalysisResult.processing_time_ms.isnot(None))
        .scalar()
        or 0.0
    )

    total_analyses = db.query(func.count(AnalysisResult.id)).scalar() or 0

    reviews = db.query(Review).all()

    if not reviews:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "avg_latency_ms": round(float(avg_latency), 2),
            "human_agreement_rate": 0.0,
            "total_analyses": total_analyses,
            "total_reviews": 0,
            "needs_reviews": True,
        }

    correct = sum(1 for r in reviews if r.ai_was_correct == 1)
    total = len(reviews)

    accuracy = (correct / total) * 100 if total > 0 else 0

    tp = sum(1 for r in reviews if r.ai_was_correct == 1 and r.decision == "approve")
    fp = sum(1 for r in reviews if r.ai_was_correct == 0 and r.decision == "reject")
    fn = sum(1 for r in reviews if r.ai_was_correct == 0 and r.decision == "approve")

    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
    f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    return {
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1_score, 2),
        "avg_latency_ms": round(float(avg_latency), 2),
        "human_agreement_rate": round(accuracy, 2),
        "total_analyses": total_analyses,
        "total_reviews": total,
        "needs_reviews": False,
    }


@router.get("/trends")
async def get_trends(days: int = 7, db: Session = Depends(get_db)):
    """Get trend data over time"""
    since_date = datetime.now() - timedelta(days=days)

    date_func = func.date(Content.created_at)
    date_func_analysis = func.date(AnalysisResult.analysis_timestamp)

    daily_data = (
        db.query(date_func.label("date"), func.count(Content.id).label("count"))
        .filter(Content.created_at >= since_date, Content.status == "completed")
        .group_by(date_func)
        .all()
    )

    deepfake_data = (
        db.query(date_func_analysis.label("date"), func.count(AnalysisResult.id).label("count"))
        .filter(
            AnalysisResult.analysis_timestamp >= since_date,
            AnalysisResult.is_deepfake == 1,
        )
        .group_by(date_func_analysis)
        .all()
    )

    return {
        "content_analyzed": [{"date": str(d.date), "count": d.count} for d in daily_data],
        "deepfakes_detected": [{"date": str(d.date), "count": d.count} for d in deepfake_data],
    }


@router.post("/seed-demo")
async def seed_demo_data(db: Session = Depends(get_db)):
    """Seed the database with demo data for analytics visualization"""
    import hashlib

    content_types = ["text", "image", "video", "audio"]
    risk_levels = ["low", "medium", "high", "critical"]
    fact_statuses = ["True", "False", "Misleading", "Partially True", "Unverified"]

    created_count = 0

    for days_ago in range(6, -1, -1):
        num_items = random.randint(3, 8)
        for _ in range(num_items):
            c_type = random.choice(content_types)
            ts = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))

            content = Content(
                content_type=c_type,
                file_name=f"demo_{c_type}_{created_count}.{'jpg' if c_type == 'image' else 'mp4' if c_type == 'video' else 'txt'}",
                status="completed",
                digital_fingerprint=hashlib.sha256(f"demo_{created_count}".encode()).hexdigest(),
                created_at=ts,
            )
            db.add(content)
            db.flush()

            is_deepfake = 1 if random.random() < 0.15 else 0
            risk = random.choice(risk_levels)
            fact_status = random.choice(fact_statuses)
            confidence = round(random.uniform(0.3, 0.95), 2)
            processing_ms = random.randint(800, 12000)

            analysis = AnalysisResult(
                content_id=content.id,
                is_deepfake=is_deepfake,
                deepfake_confidence=round(random.uniform(0.1, 0.9), 2) if is_deepfake else round(random.uniform(0.01, 0.3), 2),
                is_manipulated=is_deepfake,
                fact_check_status=fact_status,
                fact_check_confidence=confidence,
                explanation=f"Demo analysis: {fact_status} with {confidence:.0%} confidence.",
                risk_level=risk,
                overall_confidence=confidence,
                processing_time_ms=processing_ms,
                analysis_timestamp=ts,
            )
            db.add(analysis)
            db.flush()

            # Add reviews for ~60% of content
            if random.random() < 0.60:
                ai_correct = 1 if random.random() < 0.82 else 0
                decision = random.choice(["approve", "reject", "flag"])
                review = Review(
                    content_id=content.id,
                    analysis_id=analysis.id,
                    reviewer_id=f"reviewer_{random.randint(1, 5)}",
                    reviewer_name=random.choice(["Dr. Smith", "Alex Johnson", "Priya Patel", "Maria Garcia", "James Chen"]),
                    decision=decision,
                    ai_was_correct=ai_correct,
                    feedback_notes="Demo review" if random.random() < 0.5 else None,
                    review_timestamp=ts + timedelta(hours=random.randint(1, 24)),
                )
                db.add(review)

            created_count += 1

    db.commit()

    return {
        "status": "success",
        "message": f"Seeded {created_count} demo content items with analyses and reviews across 7 days.",
        "items_created": created_count,
    }
