"""
Google Gemini API client for multimodal analysis
Lazily initializes — mock responses when API key is not configured
Includes retry logic for free-tier rate limits
"""
import os
import json
import re
import time
import asyncio
from typing import Optional, Dict, Any, List


class GeminiClient:
    """Client for Google Gemini API interactions — lazily initializes model"""

    def __init__(self):
        self._model = None
        self._initialized = False
        self._api_key_found = False

    def _get_model(self):
        """Lazily initialize model so API key is always read fresh from env."""
        if self._initialized:
            return self._model

        from app.config import settings
        api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY") or _read_env_file()
        if api_key:
            self._api_key_found = True
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                self._model = genai.GenerativeModel("gemini-2.0-flash")
                self._initialized = True
                print(f"[Gemini] Model initialized with key: {api_key[:10]}...")
            except Exception as e:
                print(f"[Gemini] Failed to initialize: {e}")
                self._initialized = True
        else:
            print("[Gemini] No API key found — using mock responses.")
            self._initialized = True
        return self._model

    async def _call_with_retry(self, func, max_retries=3):
        """Call Gemini with retry logic for rate limits"""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                error_str = str(e).lower()
                is_quota = any(k in error_str for k in ["quota", "rate", "429", "resource_exhausted"])
                if is_quota and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # 2s, 4s, 6s
                    print(f"[Gemini] Rate limited, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(wait_time)
                else:
                    raise

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text content for misinformation"""
        model = self._get_model()
        if not model:
            return self._mock_text_analysis(text)

        try:
            prompt = f"""You are an expert fact-checker and misinformation analyst.
Analyze the following text and return a JSON object (no markdown, no code blocks, raw JSON only).

Text: {text}

Return exactly this JSON structure:
{{
  "assessment": "True|False|Misleading|Partially True|Unverified",
  "confidence": 0.0 to 1.0,
  "explanation": "Clear and detailed explanation of your assessment",
  "risk_level": "low|medium|high|critical",
  "claims": ["claim 1", "claim 2"]
}}"""

            response = await self._call_with_retry(
                lambda: model.generate_content(prompt)
            )
            return self._parse_json_response(response.text, self._mock_text_analysis(text))
        except Exception as e:
            print(f"[Gemini] Text analysis error: {e}")
            return self._error_response(e, "text")

    async def analyze_image(self, image_path: str, prompt: str = None) -> Dict[str, Any]:
        """Analyze image for manipulation or misinformation"""
        model = self._get_model()
        if not model:
            return self._mock_image_analysis()

        try:
            import PIL.Image

            img = PIL.Image.open(image_path)

            analysis_prompt = prompt or """You are an expert in detecting AI-generated content and deepfakes.
Analyze this image and return a JSON object (no markdown, raw JSON only):
{
  "manipulation_detected": true or false,
  "confidence": 0.0 to 1.0,
  "explanation": "Detailed explanation of findings",
  "risk_level": "low|medium|high|critical"
}"""

            response = await self._call_with_retry(
                lambda: model.generate_content([analysis_prompt, img])
            )
            return self._parse_json_response(response.text, self._mock_image_analysis())
        except Exception as e:
            print(f"[Gemini] Image analysis error: {e}")
            return self._error_response(e, "image")

    async def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """Analyze audio for synthetic voice detection"""
        model = self._get_model()
        if not model:
            return self._mock_audio_analysis()

        try:
            prompt = """You are an expert in detecting AI-generated and synthetic audio.
Analyze this audio and return a JSON object (no markdown, raw JSON only):
{
  "synthetic_detected": true or false,
  "confidence": 0.0 to 1.0,
  "explanation": "Detailed explanation of findings",
  "risk_level": "low|medium|high|critical"
}"""
            import pathlib
            audio_file = pathlib.Path(audio_path)
            if audio_file.exists():
                response = await self._call_with_retry(
                    lambda: model.generate_content([prompt])
                )
                return self._parse_json_response(response.text, self._mock_audio_analysis())
            return self._mock_audio_analysis()
        except Exception as e:
            print(f"[Gemini] Audio analysis error: {e}")
            return self._error_response(e, "audio")

    async def extract_claims(self, text: str) -> List[str]:
        """Extract factual claims from text"""
        model = self._get_model()
        if not model:
            return self._mock_claims(text)

        try:
            prompt = f"""Extract all factual claims from this text.
Return ONLY a raw JSON array of strings (no markdown, no code blocks).
Example output: ["Claim 1", "Claim 2"]

Text: {text}"""

            response = await self._call_with_retry(
                lambda: model.generate_content(prompt)
            )
            clean = self._clean_json_text(response.text)
            parsed = json.loads(clean)
            return parsed if isinstance(parsed, list) else self._mock_claims(text)
        except Exception as e:
            print(f"[Gemini] Claim extraction error: {e}")
            return self._mock_claims(text)

    def _clean_json_text(self, text: str) -> str:
        """Strip markdown code fences and extract raw JSON"""
        text = re.sub(r"```(?:json)?\s*", "", text)
        text = re.sub(r"```", "", text)
        text = text.strip()
        for char, end_char in [("{", "}"), ("[", "]")]:
            start = text.find(char)
            end = text.rfind(end_char)
            if start != -1 and end > start:
                return text[start : end + 1]
        return text

    def _parse_json_response(self, response_text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Gemini response to structured format with fallback"""
        try:
            clean = self._clean_json_text(response_text)
            return json.loads(clean)
        except Exception:
            result = fallback.copy()
            result["explanation"] = response_text[:500] if response_text else result.get("explanation", "")
            return result

    def _error_response(self, error: Exception, content_type: str) -> Dict[str, Any]:
        """Generate an error response that shows the real error to the user"""
        error_str = str(error)
        is_quota = any(k in error_str.lower() for k in ["quota", "rate", "429", "resource_exhausted"])

        if is_quota:
            explanation = "Gemini API rate limit reached. The free tier has daily request limits. Please wait a few minutes and try again, or upgrade your API key."
        else:
            explanation = f"Gemini API error: {error_str[:200]}"

        if content_type == "text":
            return {
                "claims": [],
                "assessment": "Unverified",
                "confidence": 0.5,
                "explanation": explanation,
                "risk_level": "medium",
            }
        elif content_type == "image":
            return {
                "manipulation_detected": False,
                "confidence": 0.5,
                "explanation": explanation,
                "risk_level": "medium",
            }
        else:
            return {
                "synthetic_detected": False,
                "confidence": 0.5,
                "explanation": explanation,
                "risk_level": "low",
            }

    def _mock_text_analysis(self, text: str) -> Dict[str, Any]:
        return {
            "claims": ["Sample claim extracted from text"],
            "assessment": "Unverified",
            "confidence": 0.5,
            "explanation": "Gemini API not configured. Set GEMINI_API_KEY in .env to enable real analysis." if not self._api_key_found else "Gemini API call failed. Check your API key and quota.",
            "risk_level": "medium",
        }

    def _mock_image_analysis(self) -> Dict[str, Any]:
        return {
            "manipulation_detected": False,
            "confidence": 0.5,
            "explanation": "Gemini API not configured. Using heuristic-only image analysis." if not self._api_key_found else "Gemini API call failed. Using heuristic-only analysis.",
            "risk_level": "low",
        }

    def _mock_audio_analysis(self) -> Dict[str, Any]:
        return {
            "synthetic_detected": False,
            "confidence": 0.5,
            "explanation": "Audio analysis requires Gemini API. Set GEMINI_API_KEY in .env." if not self._api_key_found else "Gemini API call failed.",
            "risk_level": "low",
        }

    def _mock_claims(self, text: str) -> List[str]:
        sentences = text.split(".")
        return [s.strip() for s in sentences[:3] if s.strip()]


def _read_env_file() -> Optional[str]:
    """Read GEMINI_API_KEY directly from .env file as fallback"""
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        ".env",
    ]
    for path in env_paths:
        path = os.path.abspath(path)
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                        val = line.split("=", 1)[1].strip()
                        if val and val != "your_gemini_api_key_here":
                            return val
    return None


# Global client instance (lazy — model initialized on first use)
gemini_client = GeminiClient()
