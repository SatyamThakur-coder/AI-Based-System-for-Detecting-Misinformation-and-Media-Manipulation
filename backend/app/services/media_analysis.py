"""
Media Analysis Service - Orchestrates multimodal content analysis
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional
from PIL import Image
from app.ml.deepfake_detector import deepfake_detector
from app.ml.gemini_client import gemini_client
from app.config import settings


class MediaAnalysisService:
    """Service for analyzing uploaded media"""

    async def analyze_content(
        self,
        content_type: str,
        file_path: Optional[str] = None,
        text_content: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze content based on type"""
        start_time = datetime.now()

        try:
            if content_type == "text":
                result = await self._analyze_text(text_content or "")
            elif content_type == "image":
                result = await self._analyze_image(file_path)
            elif content_type == "video":
                result = await self._analyze_video(file_path)
            elif content_type == "audio":
                result = await self._analyze_audio(file_path)
            elif content_type == "url":
                result = await self._analyze_url(url)
            else:
                result = self._default_result()
        except Exception as e:
            print(f"[MediaAnalysis] Error analyzing {content_type}: {e}")
            result = self._default_result()
            result["explanation"] = f"Analysis error: {str(e)}"

        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        result["processing_time_ms"] = processing_time
        return result

    async def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text content"""
        gemini_result = await gemini_client.analyze_text(text)
        claims = await gemini_client.extract_claims(text)

        return {
            "is_deepfake": 0,
            "deepfake_confidence": 0.0,
            "is_manipulated": 0,
            "manipulation_type": None,
            "fact_check_status": gemini_result.get("assessment", "Unverified"),
            "fact_check_confidence": gemini_result.get("confidence", 0.5),
            "claims_extracted": claims,
            "explanation": gemini_result.get("explanation", "Text analyzed for claims."),
            "risk_level": gemini_result.get("risk_level", "medium"),
            "overall_confidence": gemini_result.get("confidence", 0.5),
        }

    async def _analyze_image(self, file_path: str) -> Dict[str, Any]:
        """Analyze image for deepfakes and manipulation"""
        deepfake_result = await deepfake_detector.analyze_image(file_path)
        gemini_result = await gemini_client.analyze_image(file_path)
        metadata = self._extract_image_metadata(file_path)

        is_manipulated = deepfake_result["is_deepfake"]
        confidence = max(deepfake_result["confidence"], gemini_result.get("confidence", 0))

        return {
            "is_deepfake": is_manipulated,
            "deepfake_confidence": deepfake_result["confidence"],
            "deepfake_features": deepfake_result.get("features_detected", {}),
            "is_manipulated": is_manipulated,
            "manipulation_type": deepfake_result.get("manipulation_type"),
            "manipulation_regions": [],
            "metadata": metadata,
            "explanation": deepfake_result.get("explanation", "Image analysis completed."),
            "risk_level": self._calculate_risk_level(confidence),
            "overall_confidence": confidence,
        }

    async def _analyze_video(self, file_path: str) -> Dict[str, Any]:
        """Analyze video for deepfakes"""
        deepfake_result = await deepfake_detector.analyze_video(file_path)
        is_manipulated = deepfake_result["is_deepfake"]
        confidence = deepfake_result["confidence"]

        return {
            "is_deepfake": is_manipulated,
            "deepfake_confidence": confidence,
            "is_manipulated": is_manipulated,
            "manipulation_type": deepfake_result.get("manipulation_type"),
            "frames_analyzed": deepfake_result.get("frames_analyzed", 0),
            "explanation": deepfake_result.get("explanation", "Video analysis completed."),
            "risk_level": self._calculate_risk_level(confidence),
            "overall_confidence": confidence,
        }

    async def _analyze_audio(self, file_path: str) -> Dict[str, Any]:
        """Analyze audio for synthetic voice"""
        gemini_result = await gemini_client.analyze_audio(file_path)

        return {
            "is_deepfake": 1 if gemini_result.get("synthetic_detected") else 0,
            "deepfake_confidence": gemini_result.get("confidence", 0.0),
            "is_manipulated": 1 if gemini_result.get("synthetic_detected") else 0,
            "manipulation_type": "synthetic_voice" if gemini_result.get("synthetic_detected") else None,
            "explanation": gemini_result.get("explanation", "Audio analysis completed."),
            "risk_level": gemini_result.get("risk_level", "low"),
            "overall_confidence": gemini_result.get("confidence", 0.5),
        }

    async def _analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze content from URL"""
        try:
            import httpx

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)
                text_content = response.text[:5000]

            gemini_result = await gemini_client.analyze_text(text_content)
            return {
                "is_deepfake": 0,
                "deepfake_confidence": 0.0,
                "is_manipulated": 0,
                "fact_check_status": gemini_result.get("assessment", "Unverified"),
                "fact_check_confidence": gemini_result.get("confidence", 0.5),
                "explanation": gemini_result.get("explanation", f"URL content analyzed from {url}"),
                "risk_level": gemini_result.get("risk_level", "medium"),
                "overall_confidence": gemini_result.get("confidence", 0.5),
            }
        except Exception as e:
            return {
                "is_deepfake": 0,
                "deepfake_confidence": 0.0,
                "is_manipulated": 0,
                "explanation": f"Could not fetch URL content: {str(e)}",
                "risk_level": "medium",
                "overall_confidence": 0.5,
            }

    def _extract_image_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract EXIF and metadata from image"""
        try:
            from PIL.ExifTags import TAGS

            image = Image.open(file_path)
            exif_data = {}

            if hasattr(image, "_getexif") and image._getexif():
                exif = image._getexif()
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_data[str(tag)] = str(value)

            return {
                "format": image.format,
                "size": list(image.size),
                "mode": image.mode,
                "exif": exif_data,
                "potentially_tampered": len(exif_data) == 0,
            }
        except Exception as e:
            return {"error": str(e), "potentially_tampered": False}

    def _calculate_risk_level(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "critical"
        elif confidence >= 0.6:
            return "high"
        elif confidence >= 0.4:
            return "medium"
        else:
            return "low"

    def _default_result(self) -> Dict[str, Any]:
        return {
            "is_deepfake": -1,
            "deepfake_confidence": 0.0,
            "is_manipulated": -1,
            "explanation": "Analysis not available for this content type.",
            "risk_level": "unknown",
            "overall_confidence": 0.0,
        }


# Global service instance
media_analysis_service = MediaAnalysisService()
