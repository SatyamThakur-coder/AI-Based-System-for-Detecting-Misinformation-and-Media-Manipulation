"""
FastAPI Main Application Entry Point
AI FactGuard Studio v2.0 — rebuilt with SQLite default
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from app.config import settings
from app.db.database import init_db, get_db
from app.api import analyze, review, analytics
from app.models import Content, AnalysisResult
from app.services.provenance import provenance_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: create database tables
    print(f"[FactGuard] Starting AI FactGuard Studio v{settings.APP_VERSION}")
    print(f"[FactGuard] Database: {settings.DATABASE_URL}")
    init_db()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    print("[FactGuard] Database tables created / verified")
    print(f"[FactGuard] Upload directory: {os.path.abspath(settings.UPLOAD_DIR)}")
    yield
    # Shutdown
    print("[FactGuard] Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered platform for combating misinformation and deepfakes",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router)
app.include_router(review.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "database": "sqlite" if settings.is_sqlite else "postgresql",
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with real DB connectivity test"""
    try:
        db.execute(
            __import__("sqlalchemy").text("SELECT 1")
        )
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "database_type": "sqlite" if settings.is_sqlite else "postgresql",
        "version": settings.APP_VERSION,
    }


@app.get("/api/provenance/{content_id}")
async def get_provenance(content_id: int, db: Session = Depends(get_db)):
    """Get provenance certificate for analyzed content"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.content_id == content_id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this content")

    analysis_dict = {
        "is_deepfake": analysis.is_deepfake,
        "is_manipulated": analysis.is_manipulated,
        "overall_confidence": analysis.overall_confidence,
        "risk_level": analysis.risk_level,
        "fact_check_status": analysis.fact_check_status,
    }

    certificate = provenance_service.generate_authenticity_certificate(
        content_id=content_id,
        fingerprint=content.digital_fingerprint or "N/A",
        analysis_result=analysis_dict,
    )

    return {
        "content_id": content_id,
        "content_type": content.content_type,
        "file_name": content.file_name,
        "certificate": certificate,
    }


@app.get("/api/content/recent")
async def get_recent_content(limit: int = 10, db: Session = Depends(get_db)):
    """Get recently analyzed content"""
    items = (
        db.query(Content)
        .filter(Content.status == "completed")
        .order_by(Content.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "items": [
            {
                "id": item.id,
                "content_type": item.content_type,
                "file_name": item.file_name,
                "status": item.status,
                "created_at": item.created_at.isoformat() if item.created_at else None,
            }
            for item in items
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
