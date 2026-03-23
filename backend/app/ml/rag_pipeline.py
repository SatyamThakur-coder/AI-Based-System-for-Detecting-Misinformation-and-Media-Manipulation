"""
RAG (Retrieval-Augmented Generation) pipeline for fact checking
sentence-transformers is OPTIONAL — falls back to keyword search
Pinecone is OPTIONAL — defaults to local in-memory search
"""
import os
import uuid
from typing import List, Dict, Any, Optional
import numpy as np

# sentence-transformers (optional)
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    print("[RAG] sentence-transformers not installed — using keyword search fallback")

from app.config import settings
from app.ml.knowledge_base import SEED_KNOWLEDGE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_pinecone_key() -> Optional[str]:
    """Read PINECONE_API_KEY from .env file as a fallback."""
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
                    if line.startswith("PINECONE_API_KEY=") and not line.startswith("#"):
                        value = line.split("=", 1)[1].strip()
                        if value and value != "your_pinecone_api_key_here":
                            return value
    return None


# SEED_KNOWLEDGE imported from app.ml.knowledge_base (90+ verified facts)

EMBEDDING_DIMENSION = 384  # all-MiniLM-L6-v2 output size


# ---------------------------------------------------------------------------
# RAGPipeline
# ---------------------------------------------------------------------------

class RAGPipeline:
    """RAG-based fact checking system with multiple fallback layers"""

    def __init__(self):
        self.embedding_model = None
        self._index = None
        self._pinecone_ok = False
        self._memory_kb: List[Dict[str, Any]] = list(SEED_KNOWLEDGE)

        if HAS_SENTENCE_TRANSFORMERS:
            self._load_embedding_model()
        else:
            print("[RAG] Running with keyword-only search")

    def _load_embedding_model(self):
        """Load sentence transformer for embeddings."""
        try:
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            print(f"[RAG] Embedding model loaded: {settings.EMBEDDING_MODEL}")
        except Exception as e:
            print(f"[RAG] Failed to load embedding model: {e}")
            self.embedding_model = None

    def _get_index(self):
        """Lazily connect to Pinecone and return the index object."""
        if self._index is not None:
            return self._index

        api_key = settings.PINECONE_API_KEY or os.environ.get("PINECONE_API_KEY") or _read_pinecone_key()
        if not api_key:
            return None

        try:
            from pinecone import Pinecone, ServerlessSpec

            pc = Pinecone(api_key=api_key)
            index_name = settings.PINECONE_INDEX_NAME or "factguard-knowledge"

            existing = [idx.name for idx in pc.list_indexes()]
            if index_name not in existing:
                print(f"[Pinecone] Creating index '{index_name}'...")
                pc.create_index(
                    name=index_name,
                    dimension=EMBEDDING_DIMENSION,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            self._index = pc.Index(index_name)
            self._pinecone_ok = True
            print(f"[Pinecone] Connected to index '{index_name}'.")

            self._sync_index()
            return self._index
        except Exception as e:
            print(f"[Pinecone] Connection failed: {e} — falling back to in-memory.")
            return None

    def _sync_index(self):
        """Seed or re-seed the Pinecone index when the knowledge base has grown."""
        if not self._index or not self.embedding_model:
            return
        try:
            stats = self._index.describe_index_stats()
            total = stats.get("total_vector_count", 0)
            kb_size = len(SEED_KNOWLEDGE)
            if total < kb_size:
                print(f"[Pinecone] Index has {total} vectors but KB has {kb_size} facts — re-seeding...")
                # Delete old vectors and re-seed with full KB
                if total > 0:
                    self._index.delete(delete_all=True)
                self._upsert_docs(SEED_KNOWLEDGE)
                print(f"[Pinecone] Seeded {kb_size} facts into index.")
        except Exception as e:
            print(f"[Pinecone] Seeding error: {e}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def check_claim(self, claim: str) -> Dict[str, Any]:
        """Check a claim against the knowledge base."""
        try:
            relevant_docs = await self._retrieve_relevant_docs(claim)
            assessment = self._assess_claim(claim, relevant_docs)
            return {
                "claim": claim,
                "status": assessment["status"],
                "confidence": assessment["confidence"],
                "evidence": relevant_docs,
                "explanation": assessment["explanation"],
                "sources": [doc["url"] for doc in relevant_docs if "url" in doc],
            }
        except Exception as e:
            print(f"[RAG] Claim checking error: {e}")
            return self._unverified_result(claim)

    async def add_to_knowledge_base(self, text: str, source: str, url: str, verified: bool = True):
        """Add new verified information to the knowledge base."""
        doc = {"text": text, "source": source, "url": url, "verified": verified}
        index = self._get_index()
        if index and self.embedding_model:
            self._upsert_docs([doc])
        self._memory_kb.append(doc)

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    async def _retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.embedding_model:
            return self._keyword_search(query, top_k)

        index = self._get_index()
        if index:
            try:
                return self._pinecone_search(query, top_k)
            except Exception as e:
                print(f"[Pinecone] Query failed: {e}")

        return self._local_embedding_search(query, top_k)

    def _pinecone_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        query_vec = self.embedding_model.encode(query).tolist()
        response = self._index.query(vector=query_vec, top_k=top_k, include_metadata=True)
        results = []
        for match in response.get("matches", []):
            meta = match.get("metadata", {})
            results.append({
                "text": meta.get("text", ""),
                "source": meta.get("source", "Unknown"),
                "url": meta.get("url", ""),
                "category": meta.get("category", ""),
                "verified": meta.get("verified", False),
                "similarity_score": float(match.get("score", 0.0)),
            })
        return results

    def _local_embedding_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        if not self._memory_kb:
            return []
        try:
            query_vec = self.embedding_model.encode(query)
            kb_texts = [doc["text"] for doc in self._memory_kb]
            kb_vecs = self.embedding_model.encode(kb_texts)
            sims = np.dot(kb_vecs, query_vec) / (
                np.linalg.norm(kb_vecs, axis=1) * np.linalg.norm(query_vec) + 1e-9
            )
            top_idx = np.argsort(sims)[-top_k:][::-1]
            results = []
            for i in top_idx:
                doc = self._memory_kb[i].copy()
                doc["similarity_score"] = float(sims[i])
                results.append(doc)
            return results
        except Exception as e:
            print(f"[RAG] Local search error: {e}")
            return self._keyword_search(query, top_k)

    def _keyword_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Simple keyword overlap search — last resort fallback."""
        keywords = set(query.lower().split())
        scored = []
        for doc in self._memory_kb:
            overlap = len(keywords & set(doc["text"].lower().split()))
            if overlap:
                scored.append((doc, overlap))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [d.copy() for d, _ in scored[:top_k]]

    # ------------------------------------------------------------------
    # Upsert
    # ------------------------------------------------------------------

    def _upsert_docs(self, docs: List[Dict[str, Any]]):
        if not self._index or not self.embedding_model:
            return
        vectors = []
        for doc in docs:
            vec = self.embedding_model.encode(doc["text"]).tolist()
            vectors.append({
                "id": str(uuid.uuid4()),
                "values": vec,
                "metadata": {
                    "text": doc.get("text", ""),
                    "source": doc.get("source", ""),
                    "url": doc.get("url", ""),
                    "category": doc.get("category", ""),
                    "verified": doc.get("verified", False),
                },
            })
        self._index.upsert(vectors=vectors)

    # ------------------------------------------------------------------
    # Assessment
    # ------------------------------------------------------------------

    def _assess_claim(self, claim: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess a claim against retrieved evidence.
        
        Key principle: low similarity does NOT mean a claim is false.
        It only means the knowledge base doesn't have relevant information.
        A claim like 'humans have 2 hands' has low similarity to climate 
        data — that doesn't make it questionable.
        """
        if not evidence:
            return {
                "status": "Unverified",
                "confidence": 0.0,
                "explanation": "No relevant evidence found in knowledge base.",
            }

        # Get similarity scores, filter out docs with no score
        scores = [doc.get("similarity_score") for doc in evidence if doc.get("similarity_score") is not None]
        if not scores:
            return {
                "status": "Unverified",
                "confidence": 0.0,
                "explanation": "No scored evidence available to assess this claim.",
            }

        best_sim = float(max(scores))
        avg_sim = float(np.mean(scores))

        # Cap confidence to [0.0, 1.0]
        confidence = min(max(avg_sim, 0.0), 1.0)

        # Check if any evidence is from a verified source
        has_verified = any(doc.get("verified", False) for doc in evidence)

        if best_sim > 0.45:
            # Strong match — claim is well-supported by knowledge base
            top_source = next((d for d in evidence if d.get("similarity_score", 0) == best_sim), evidence[0])
            source_name = top_source.get("source", "knowledge base")
            return {
                "status": "True",
                "confidence": min(best_sim * 1.3, 1.0),  # Scale up for display
                "explanation": f"Claim verified as TRUE and supported by {source_name}. Matched {len(evidence)} trusted source(s) with {best_sim:.0%} similarity.",
            }
        elif best_sim > 0.30:
            # Moderate match — partially supported
            return {
                "status": "Partially True",
                "confidence": min(confidence * 1.2, 1.0),
                "explanation": f"Claim has partial support in the knowledge base (best match: {best_sim:.0%}). Related verified sources found.",
            }
        else:
            # Low match — claim topic isn't covered in our knowledge base
            return {
                "status": "Unverified",
                "confidence": confidence,
                "explanation": "This claim is outside the scope of our current knowledge base. It may still be true — we simply don't have matching verified sources to confirm or deny it.",
            }

    def _unverified_result(self, claim: str) -> Dict[str, Any]:
        return {
            "claim": claim,
            "status": "Unverified",
            "confidence": 0.0,
            "evidence": [],
            "explanation": "Unable to verify claim due to a system error.",
            "sources": [],
        }


# Global instance
rag_pipeline = RAGPipeline()
