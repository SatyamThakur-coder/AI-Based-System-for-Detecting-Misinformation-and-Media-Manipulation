"""
Analysis API endpoints
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import hashlib
from datetime import datetime
from app.db.database import get_db
from app.models import Content, AnalysisResult
from app.services.media_analysis import media_analysis_service
from app.services.fact_checking import fact_checking_service
from app.services.provenance import provenance_service
from app.utils.file_handler import save_upload_file, get_content_type

router = APIRouter(prefix="/api/analyze", tags=["analysis"])


@router.post("/upload", response_model=dict)
async def upload_and_analyze(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """Upload and analyze content"""

    # Determine content type
    if file:
        content_type = get_content_type(file.filename)
        file_name = file.filename
    elif text:
        content_type = "text"
        file_name = None
    elif url:
        content_type = "url"
        file_name = None
    else:
        raise HTTPException(status_code=400, detail="No content provided. Send a file, text, or URL.")

    # Create content record
    content = Content(
        content_type=content_type,
        text_content=text,
        source_url=url,
        file_name=file_name,
        status="processing",
    )
    db.add(content)
    db.commit()
    db.refresh(content)

    # Save file if provided
    file_path = None
    if file:
        file_path, file_size = await save_upload_file(file, content.id)
        content.file_path = file_path
        content.file_size = file_size
        content.digital_fingerprint = provenance_service.generate_fingerprint(file_path)
    else:
        content.digital_fingerprint = hashlib.sha256(
            (text or url or str(datetime.now())).encode()
        ).hexdigest()

    db.commit()

    # Perform analysis
    try:
        analysis_result = await media_analysis_service.analyze_content(
            content_type=content_type,
            file_path=file_path,
            text_content=text,
            url=url,
        )

        # If text, also run fact-checking via RAG/Pinecone pipeline
        if content_type == "text" and text:
            fact_check_result = await fact_checking_service.check_claims(text)
            analysis_result["fact_check_status"] = fact_check_result["overall_status"]
            analysis_result["fact_check_confidence"] = fact_check_result["confidence"]
            analysis_result["claims_extracted"] = [c["claim"] for c in fact_check_result["claims"]]
            analysis_result["evidence_sources"] = fact_check_result["claims"]

            # Collect news articles from all claims
            all_news = []
            for c in fact_check_result["claims"]:
                all_news.extend(c.get("news_articles", []))
            if all_news:
                analysis_result["news_articles"] = all_news[:5]

            # Use RAG/news results for explanation when Gemini is rate-limited
            gemini_explanation = analysis_result.get("explanation", "")
            is_gemini_error = any(k in (gemini_explanation or "").lower() for k in [
                "not configured", "rate limit", "quota", "api error"
            ])
            if is_gemini_error and fact_check_result["claims"]:
                rag_explanations = []
                for c in fact_check_result["claims"]:
                    rag_explanations.append(
                        f"Claim: \"{c['claim']}\" → {c['status']} "
                        f"(confidence: {c['confidence']:.0%}). {c.get('explanation', '')}"
                    )
                analysis_result["explanation"] = (
                    "Fact-checked via RAG knowledge base (Pinecone). "
                    + " | ".join(rag_explanations)
                )
                # Update risk and confidence from RAG results
                analysis_result["overall_confidence"] = fact_check_result["confidence"]
                if fact_check_result["overall_status"] in ("False", "Misleading"):
                    analysis_result["risk_level"] = "high"
                elif fact_check_result["overall_status"] == "True":
                    analysis_result["risk_level"] = "low"

        # Save analysis result
        analysis = AnalysisResult(
            content_id=content.id,
            is_deepfake=analysis_result.get("is_deepfake", -1),
            deepfake_confidence=analysis_result.get("deepfake_confidence", 0.0),
            deepfake_features=analysis_result.get("deepfake_features"),
            is_manipulated=analysis_result.get("is_manipulated", -1),
            manipulation_type=analysis_result.get("manipulation_type"),
            manipulation_regions=analysis_result.get("manipulation_regions"),
            fact_check_status=analysis_result.get("fact_check_status"),
            fact_check_confidence=analysis_result.get("fact_check_confidence"),
            claims_extracted=analysis_result.get("claims_extracted"),
            evidence_sources=analysis_result.get("evidence_sources"),
            explanation=analysis_result.get("explanation", "Analysis completed."),
            features_triggered=analysis_result.get("features_triggered"),
            risk_level=analysis_result.get("risk_level", "unknown"),
            overall_confidence=analysis_result.get("overall_confidence", 0.0),
            processing_time_ms=analysis_result.get("processing_time_ms"),
        )
        db.add(analysis)

        content.status = "completed"
        db.commit()
        db.refresh(analysis)

        return {
            "content_id": content.id,
            "analysis_id": analysis.id,
            "status": "success",
            "result": {
                "is_deepfake": analysis.is_deepfake,
                "deepfake_confidence": analysis.deepfake_confidence,
                "is_manipulated": analysis.is_manipulated,
                "manipulation_type": analysis.manipulation_type,
                "fact_check_status": analysis.fact_check_status,
                "fact_check_confidence": analysis.fact_check_confidence,
                "claims": analysis.claims_extracted,
                "evidence": analysis.evidence_sources,
                "explanation": analysis.explanation,
                "risk_level": analysis.risk_level,
                "overall_confidence": analysis.overall_confidence,
                "processing_time_ms": analysis.processing_time_ms,
                "news_articles": analysis_result.get("news_articles", []),
            },
        }

    except Exception as e:
        content.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/{content_id}", response_model=dict)
async def get_analysis(content_id: int, db: Session = Depends(get_db)):
    """Get analysis results for content"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    analysis = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.content_id == content_id)
        .first()
    )

    if not analysis:
        return {"content_id": content_id, "status": content.status, "result": None}

    return {
        "content_id": content_id,
        "status": content.status,
        "result": {
            "analysis_id": analysis.id,
            "is_deepfake": analysis.is_deepfake,
            "deepfake_confidence": analysis.deepfake_confidence,
            "is_manipulated": analysis.is_manipulated,
            "fact_check_status": analysis.fact_check_status,
            "explanation": analysis.explanation,
            "risk_level": analysis.risk_level,
            "overall_confidence": analysis.overall_confidence,
        },
    }
