"""
NewsData.io integration for real-time news-based fact verification.
Uses the NewsData.io API to search for recent news articles matching claims,
providing live evidence from real news sources.
"""
import httpx
import re
from typing import List, Dict, Any, Optional
from app.config import settings


NEWSDATA_BASE_URL = "https://newsdata.io/api/1/latest"


class NewsSearchService:
    """Search live news articles to verify claims in real-time."""

    def __init__(self):
        self.api_key = settings.NEWSDATA_API_KEY
        self._available = bool(self.api_key)
        if self._available:
            print(f"[NewsData] API key configured — live news fact-checking enabled")
        else:
            print("[NewsData] No API key — live news search disabled")

    @property
    def is_available(self) -> bool:
        return self._available

    def _extract_keywords(self, claim: str, max_words: int = 5) -> str:
        """Extract the most meaningful keywords from a claim for search."""
        # Remove common stop words to get meaningful search terms
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "about", "that",
            "this", "it", "its", "and", "or", "but", "not", "no", "if", "then",
            "than", "so", "very", "just", "also", "too", "more", "most", "much",
            "many", "some", "any", "all", "each", "every", "both", "few",
            "other", "such", "only", "own", "same", "which", "what", "who",
            "whom", "how", "when", "where", "why", "there", "here", "up",
            "out", "they", "them", "we", "us", "he", "she", "him", "her",
        }
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{2,}\b', claim.lower())
        keywords = [w for w in words if w not in stop_words]
        # Take the most meaningful words (prioritize longer words as they're more specific)
        keywords.sort(key=len, reverse=True)
        return " ".join(keywords[:max_words])

    async def search_news(self, claim: str, language: str = "en") -> Dict[str, Any]:
        """
        Search NewsData.io for articles related to a claim.
        Returns matching articles with relevance assessment.
        """
        if not self._available:
            return {"articles": [], "query": "", "error": "NewsData API not configured"}

        query = self._extract_keywords(claim)
        if not query:
            return {"articles": [], "query": "", "error": "Could not extract keywords"}

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    NEWSDATA_BASE_URL,
                    params={
                        "apikey": self.api_key,
                        "q": query,
                        "language": language,
                        "size": 5,
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    articles = []
                    for article in (data.get("results") or []):
                        articles.append({
                            "title": article.get("title", ""),
                            "description": article.get("description", ""),
                            "source": article.get("source_name") or article.get("source_id", "Unknown"),
                            "url": article.get("link", ""),
                            "published": article.get("pubDate", ""),
                            "category": (article.get("category") or ["general"])[0] if article.get("category") else "general",
                            "image_url": article.get("image_url", ""),
                        })

                    return {
                        "articles": articles,
                        "query": query,
                        "total": data.get("totalResults", len(articles)),
                    }
                elif response.status_code == 401:
                    print(f"[NewsData] Invalid API key")
                    return {"articles": [], "query": query, "error": "Invalid API key"}
                elif response.status_code == 429:
                    print(f"[NewsData] Rate limited")
                    return {"articles": [], "query": query, "error": "Rate limited"}
                else:
                    print(f"[NewsData] API error {response.status_code}: {response.text[:200]}")
                    return {"articles": [], "query": query, "error": f"API error {response.status_code}"}

        except httpx.TimeoutException:
            print("[NewsData] Request timed out")
            return {"articles": [], "query": query, "error": "Request timed out"}
        except Exception as e:
            print(f"[NewsData] Error: {e}")
            return {"articles": [], "query": query, "error": str(e)}

    async def verify_claim_with_news(self, claim: str) -> Dict[str, Any]:
        """
        Verify a claim using live news articles.
        Returns structured verification result with news evidence.
        """
        result = await self.search_news(claim)
        articles = result.get("articles", [])

        if not articles:
            return {
                "has_news_evidence": False,
                "articles": [],
                "summary": "No recent news articles found related to this claim.",
                "query_used": result.get("query", ""),
            }

        # Build a summary from top articles
        sources = [a["source"] for a in articles[:3]]
        titles = [a["title"] for a in articles[:3] if a["title"]]

        summary_parts = [f"Found {len(articles)} recent news article(s) from: {', '.join(sources)}."]
        if titles:
            summary_parts.append(f"Top headline: \"{titles[0]}\"")

        return {
            "has_news_evidence": True,
            "article_count": len(articles),
            "articles": articles[:5],
            "summary": " ".join(summary_parts),
            "query_used": result.get("query", ""),
        }


# Global instance
news_search = NewsSearchService()
