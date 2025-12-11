"""Utility functions for text embedding.

Provides a centralized function to generate embeddings using OpenAI's API.
"""
from typing import List

from openai import OpenAI
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# --- OpenAI Client ---
# Initialize OpenAI client with API key from settings
openai_client = OpenAI(api_key=settings.openai_api_key)


def get_embedding(text: str) -> List[float]:
    """Generates an embedding for the given text using OpenAI.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    try:
        response = openai_client.embeddings.create(
            input=text,
            model=settings.openai_embedding_model
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise
