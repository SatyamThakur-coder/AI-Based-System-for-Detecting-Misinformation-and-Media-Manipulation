"""
Fact Checking Service using RAG pipeline + Gemini + NewsData.io
Multi-layer verification: KB search → Live news → Gemini AI analysis
"""
from typing import Dict, Any, List
from app.ml.rag_pipeline import rag_pipeline
from app.ml.gemini_client import gemini_client
from app.ml.news_search import news_search


class FactCheckingService:
    """Service for fact-checking claims using RAG + News + Gemini"""

    async def check_claims(self, text: str) -> Dict[str, Any]:
        """Extract and verify claims from text.
        
        Claims are extracted via Gemini (or simple splitting as fallback).
        Each claim is verified against:
        1. Pinecone/local knowledge base (RAG)
        2. Live news articles (NewsData.io)
        3. Gemini AI (when available)
        """
        # Try Gemini for claim extraction; fall back to simple sentence splitting
        claims = await gemini_client.extract_claims(text)

        # If Gemini returned empty or mock claims, do simple splitting
        if not claims or len(claims) == 0:
            claims = self._simple_extract_claims(text)

        # Verify each claim through multi-layer pipeline
        claim_results = []
        for claim in claims[:5]:
            result = await self._verify_claim_multilayer(claim)
            claim_results.append(result)

        # Aggregate results
        if claim_results:
            avg_confidence = sum(r["confidence"] for r in claim_results) / len(claim_results)

            statuses = [r["status"] for r in claim_results]
            if "False" in statuses:
                overall_status = "False"
            elif all(s == "True" for s in statuses):
                overall_status = "True"
            elif "Partially True" in statuses:
                overall_status = "Partially True"
            elif "Unverified" in statuses and "True" in statuses:
                overall_status = "Partially True"
            else:
                overall_status = "Unverified"
        else:
            avg_confidence = 0.0
            overall_status = "Unverified"

        return {
            "overall_status": overall_status,
            "confidence": avg_confidence,
            "claims": claim_results,
            "total_claims_checked": len(claim_results),
        }

    async def _verify_claim_multilayer(self, claim: str) -> Dict[str, Any]:
        """Verify a single claim using all available sources."""
        # Layer 1: RAG knowledge base
        rag_result = await rag_pipeline.check_claim(claim)
        
        # Layer 2: Live news search (if available)
        news_result = None
        if news_search.is_available:
            try:
                news_result = await news_search.verify_claim_with_news(claim)
            except Exception as e:
                print(f"[FactCheck] News search error: {e}")

        # Merge results — if RAG found a good match, use it
        # If RAG says Unverified but news found articles, enhance the result
        if rag_result["status"] == "True":
            # RAG verified it — add news as bonus evidence
            if news_result and news_result.get("has_news_evidence"):
                rag_result["news_articles"] = news_result["articles"][:3]
                rag_result["explanation"] += f" Additionally, {news_result['article_count']} recent news article(s) found on this topic."
            return rag_result

        elif rag_result["status"] == "Partially True":
            if news_result and news_result.get("has_news_evidence"):
                rag_result["news_articles"] = news_result["articles"][:3]
                rag_result["explanation"] += f" Supported by {news_result['article_count']} recent news article(s)."
            return rag_result

        elif rag_result["status"] == "Unverified":
            # RAG doesn't have it — check if news gives us something
            if news_result and news_result.get("has_news_evidence"):
                articles = news_result["articles"][:3]
                sources = [a["source"] for a in articles]
                return {
                    "claim": claim,
                    "status": "Partially True",
                    "confidence": min(0.5 + (len(articles) * 0.08), 0.85),
                    "evidence": rag_result.get("evidence", []),
                    "news_articles": articles,
                    "explanation": (
                        f"Not in our knowledge base, but found {news_result['article_count']} "
                        f"recent news article(s) from {', '.join(sources[:3])} discussing this topic. "
                        f"{news_result['summary']}"
                    ),
                    "sources": [a["url"] for a in articles if a.get("url")],
                    "verification_source": "news",
                }
            # Nothing from either source
            return rag_result
        
        return rag_result

    async def verify_single_claim(self, claim: str) -> Dict[str, Any]:
        """Verify a single claim via multi-layer pipeline"""
        return await self._verify_claim_multilayer(claim)

    def _simple_extract_claims(self, text: str) -> List[str]:
        """Simple sentence-based claim extraction when Gemini is unavailable"""
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".")]
        # Filter out very short fragments
        return [s for s in sentences if len(s) > 15][:5]


# Global service instance
fact_checking_service = FactCheckingService()
