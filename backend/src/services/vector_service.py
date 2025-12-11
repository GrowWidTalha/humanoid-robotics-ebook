"""Service for interacting with the Qdrant vector database.

Provides functionality to search for similar content chunks based on embeddings.
"""
from typing import List, Dict, Any, Optional

from qdrant_client import models
from src.config.database import get_qdrant_client
from src.config.settings import settings
from src.utils.embedding import get_embedding
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VectorService:
    """Handles interactions with the Qdrant vector database."""

    @staticmethod
    async def search_similar_chunks(
        query_text: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Embeds the query text and searches Qdrant for similar content chunks.

        Args:
            query_text: The text to query for.
            top_k: The number of top similar chunks to retrieve.
            filters: Optional Qdrant filters to apply (e.g., {"chapter": "Module 1"}).

        Returns:
            A list of dictionaries, where each dictionary represents a content chunk
            and its metadata.
        """
        qdrant_client = get_qdrant_client()
        
        # Get embedding for the query text
        query_vector = get_embedding(query_text)

        search_params = models.SearchParams(hnsw_ef=128, exact=False)

        # Build query filter from provided filters
        qdrant_filter: Optional[models.Filter] = None
        if filters:
            must_clauses = []
            for key, value in filters.items():
                must_clauses.append(models.FieldCondition(
                    key=key,
                    range=models.KeywordRange(exact=value)
                ))
            qdrant_filter = models.Filter(must=must_clauses)
            
        try:
            search_result = await qdrant_client.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_vector,
                query_filter=qdrant_filter,
                limit=top_k,
                search_params=search_params,
                append_payload=True,  # Ensure payload (metadata) is returned
            )

            chunks = []
            for hit in search_result:
                if hit.payload:
                    chunks.append(hit.payload)
            
            logger.info(f"Found {len(chunks)} similar chunks for query: '{query_text[:50]}...'")
            return chunks
        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            raise