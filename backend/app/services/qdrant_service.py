"""
Qdrant vector database integration for fraud pattern matching
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any, Optional
from loguru import logger
import numpy as np
from app.core.config import settings


class QdrantService:
    """Service for Qdrant vector similarity search"""

    def __init__(self):
        try:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                api_key=settings.QDRANT_API_KEY
            )
            self.collection_name = settings.QDRANT_COLLECTION
            self._ensure_collection()
        except Exception as e:
            logger.warning(f"Qdrant connection failed: {e}. Using mock mode.")
            self.client = None

    def _ensure_collection(self):
        """Ensure fraud patterns collection exists"""
        if not self.client:
            return

        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,  # Embedding dimension
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")

                # Seed with sample fraud patterns
                self._seed_fraud_patterns()
        except Exception as e:
            logger.error(f"Collection setup error: {e}")

    def _seed_fraud_patterns(self):
        """Seed database with known fraud patterns"""
        sample_patterns = [
            {
                "id": "fraud_001",
                "type": "card_fraud",
                "description": "Multiple transactions from different countries within 1 hour",
                "severity": "critical",
                "vector": self._generate_mock_embedding("rapid geographic changes multiple countries")
            },
            {
                "id": "fraud_002",
                "type": "money_laundering",
                "description": "Large transfers followed by immediate withdrawals in different currency",
                "severity": "high",
                "vector": self._generate_mock_embedding("large transfer immediate withdrawal currency conversion")
            },
            {
                "id": "fraud_003",
                "type": "identity_theft",
                "description": "Sudden change in spending patterns and new device login",
                "severity": "high",
                "vector": self._generate_mock_embedding("account takeover new device spending pattern change")
            },
            {
                "id": "fraud_004",
                "type": "synthetic_identity",
                "description": "New account with high credit limit, rapid maxing out",
                "severity": "critical",
                "vector": self._generate_mock_embedding("new account high limit rapid spending bust out")
            },
            {
                "id": "fraud_005",
                "type": "card_fraud",
                "description": "Small test transactions followed by large purchase",
                "severity": "medium",
                "vector": self._generate_mock_embedding("card testing small transactions large purchase")
            }
        ]

        points = [
            PointStruct(
                id=i,
                vector=pattern["vector"],
                payload={
                    "pattern_id": pattern["id"],
                    "type": pattern["type"],
                    "description": pattern["description"],
                    "severity": pattern["severity"]
                }
            )
            for i, pattern in enumerate(sample_patterns)
        ]

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Seeded {len(points)} fraud patterns")
        except Exception as e:
            logger.error(f"Seeding error: {e}")

    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Generate mock embedding (in production, use real embedding model)"""
        # Simple hash-based mock embedding
        np.random.seed(hash(text) % (2**32))
        return np.random.rand(384).tolist()

    async def find_similar_fraud_cases(
        self,
        transaction_embedding: List[float],
        limit: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Find similar fraud patterns in vector database
        """
        if not self.client:
            return self._mock_similar_cases()

        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=transaction_embedding,
                limit=limit,
                score_threshold=score_threshold
            )

            similar_cases = []
            for hit in search_result:
                similar_cases.append({
                    "pattern_id": hit.payload.get("pattern_id"),
                    "type": hit.payload.get("type"),
                    "description": hit.payload.get("description"),
                    "severity": hit.payload.get("severity"),
                    "similarity_score": hit.score
                })

            return similar_cases

        except Exception as e:
            logger.error(f"Qdrant search error: {e}")
            return self._mock_similar_cases()

    async def store_fraud_case(
        self,
        case_id: str,
        fraud_type: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ):
        """Store new fraud case for future similarity matching"""
        if not self.client:
            logger.info("Mock: Stored fraud case")
            return

        try:
            point = PointStruct(
                id=hash(case_id) % (2**32),
                vector=embedding,
                payload={
                    "case_id": case_id,
                    "fraud_type": fraud_type,
                    **metadata
                }
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            logger.info(f"Stored fraud case: {case_id}")

        except Exception as e:
            logger.error(f"Storage error: {e}")

    async def get_fraud_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored fraud patterns"""
        if not self.client:
            return self._mock_statistics()

        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "total_patterns": collection_info.points_count,
                "vector_dimension": collection_info.config.params.vectors.size,
                "distance_metric": collection_info.config.params.vectors.distance.value
            }
        except Exception as e:
            logger.error(f"Statistics error: {e}")
            return self._mock_statistics()

    def _mock_similar_cases(self) -> List[Dict[str, Any]]:
        """Mock similar cases for demo"""
        return [
            {
                "pattern_id": "fraud_001",
                "type": "card_fraud",
                "description": "Multiple transactions from different countries within 1 hour",
                "severity": "critical",
                "similarity_score": 0.89
            },
            {
                "pattern_id": "fraud_005",
                "type": "card_fraud",
                "description": "Small test transactions followed by large purchase",
                "severity": "medium",
                "similarity_score": 0.76
            }
        ]

    def _mock_statistics(self) -> Dict[str, Any]:
        """Mock statistics for demo"""
        return {
            "total_patterns": 1247,
            "vector_dimension": 384,
            "distance_metric": "cosine"
        }


# Singleton instance
qdrant_service = QdrantService()
