#!/usr/bin/env python3
"""
Book content embedding script

Reads markdown files from docs/ (including all nested subdirectories), chunks content by headings or word count,
generates embeddings with OpenAI, and uploads to Qdrant vector database.

Usage:
    python backend/scripts/embed_book_content.py --book-path docs/ --collection-name humanoid-robotics-book-v1
"""
import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
from uuid import uuid4

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from src.config.settings import settings
from src.utils.logger import setup_logging, get_logger

setup_logging(level="INFO")
logger = get_logger(__name__)


class BookContentChunker:
    """Chunks markdown content intelligently by headings and word limits"""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize chunker

        Args:
            chunk_size: Target chunk size in words
            overlap: Word overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_markdown(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Chunk markdown content by headings and word limits

        Args:
            content: Markdown file content
            file_path: Path to markdown file (for metadata)

        Returns:
            List of chunk dictionaries with content and metadata
        """
        chunks = []

        # Extract chapter/module name from file path
        path_obj = Path(file_path)
        chapter = self._extract_chapter_name(path_obj)

        # Split by headings (## and ###)
        sections = re.split(r'(^#{2,3}\s+.+$)', content, flags=re.MULTILINE)

        current_section_heading = "Introduction"
        current_content = []

        for i, section in enumerate(sections):
            # Check if this is a heading
            heading_match = re.match(r'^(#{2,3})\s+(.+)$', section.strip())

            if heading_match:
                # Save previous section if it has content
                if current_content:
                    section_chunks = self._chunk_section(
                        "\n".join(current_content),
                        chapter,
                        current_section_heading
                    )
                    chunks.extend(section_chunks)

                # Start new section
                current_section_heading = heading_match.group(2).strip()
                current_content = []
            else:
                # Accumulate content
                if section.strip():
                    current_content.append(section.strip())

        # Process last section
        if current_content:
            section_chunks = self._chunk_section(
                "\n".join(current_content),
                chapter,
                current_section_heading
            )
            chunks.extend(section_chunks)

        return chunks

    def _chunk_section(self, content: str, chapter: str, section: str) -> List[Dict[str, Any]]:
        """Chunk a section by word count with overlap"""
        words = content.split()
        chunks = []

        if len(words) <= self.chunk_size:
            # Section fits in one chunk
            chunks.append({
                "content": content,
                "chapter": chapter,
                "section": section,
                "heading": section,
                "chunk_index": 0,
                "word_count": len(words),
            })
        else:
            # Split into multiple chunks with overlap
            chunk_index = 0
            start = 0

            while start < len(words):
                end = start + self.chunk_size
                chunk_words = words[start:end]

                chunks.append({
                    "content": " ".join(chunk_words),
                    "chapter": chapter,
                    "section": section,
                    "heading": section,
                    "chunk_index": chunk_index,
                    "word_count": len(chunk_words),
                })

                chunk_index += 1
                start = end - self.overlap  # Overlap for context

        return chunks

    def _extract_chapter_name(self, path: Path) -> str:
        """Extract chapter/module name from file path"""
        # Try to extract from directory or filename
        parts = path.parts

        # Look for patterns like "module1-ros2", "Module 1", etc.
        for part in reversed(parts):
            if re.match(r'module[-\s]*\d+', part, re.IGNORECASE):
                return part.replace('-', ' ').title()

        # Fallback to filename without extension
        return path.stem.replace('-', ' ').replace('_', ' ').title()


class BookEmbedder:
    """Handles embedding generation and Qdrant upload"""

    def __init__(self, collection_name: str = "book_content"):
        """
        Initialize embedder

        Args:
            collection_name: Qdrant collection name
        """
        self.collection_name = collection_name
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=30,  # Set a higher timeout (seconds)
        )

    async def create_collection(self):
        """Create Qdrant collection if it doesn't exist, with improved connection error handling"""
        try:
            collections = await self.qdrant_client.get_collections()
        except Exception as e:
            logger.error(
                "\nCannot connect to Qdrant. "
                f"Error: {type(e).__name__}: {e}\n"
                "-> Please make sure your Qdrant server is running and accessible at the configured URL.\n"
                f"-> Current Qdrant URL: {settings.qdrant_url}"
            )
            logger.error("Exiting due to Qdrant connection failure.")
            import sys
            sys.exit(1)

        collection_names = [col.name for col in collections.collections]

        if self.collection_name not in collection_names:
            await self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Created collection: {self.collection_name}")
        else:
            logger.info(f"Collection already exists: {self.collection_name}")

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        response = await self.openai_client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text
        )
        return response.data[0].embedding

    async def upload_chunks(self, chunks: List[Dict[str, Any]], doc_version: str = "v1.0.0"):
        """
        Upload chunks with embeddings to Qdrant

        Args:
            chunks: List of chunk dictionaries
            doc_version: Document version identifier
        """
        logger.info(f"Uploading {len(chunks)} chunks to Qdrant...")

        points = []

        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = await self.embed_text(chunk["content"])

            # Create point
            point = PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "content": chunk["content"],
                    "chapter": chunk["chapter"],
                    "section": chunk["section"],
                    "heading": chunk["heading"],
                    "chunk_index": chunk["chunk_index"],
                    "word_count": chunk["word_count"],
                    "doc_version": doc_version,
                }
            )
            points.append(point)

            # Upload in batches of 100
            if len(points) >= 100:
                await self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logger.info(f"Uploaded batch {i // 100 + 1} ({len(points)} points)")
                points = []

        # Upload remaining points
        if points:
            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Uploaded final batch ({len(points)} points)")

    async def close(self):
        """Close connections"""
        await self.qdrant_client.close()


def get_all_markdown_files_recursively(root_path: Path) -> List[Path]:
    """
    Find all markdown files recursively (as deep as needed) in the given root_path.
    This function will walk all subdirectories and return both *.md and *.mdx files.

    Args:
        root_path: Path to the root directory

    Returns:
        List[Path]: List of all markdown file Paths
    """
    md_files = list(root_path.rglob("*.md"))
    mdx_files = list(root_path.rglob("*.mdx"))
    all_files = md_files + mdx_files
    return [file for file in all_files if file.is_file() and 'node_modules' not in str(file)]


async def main():
    """Main embedding script"""
    parser = argparse.ArgumentParser(description="Embed book content into Qdrant")
    parser.add_argument(
        "--book-path",
        type=str,
        required=True,
        help="Path to book content directory (e.g., docs/)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default="humanoid-robotics-book-v1",
        help="Qdrant collection name"
    )
    parser.add_argument(
        "--doc-version",
        type=str,
        default="v1.0.0",
        help="Document version identifier"
    )

    args = parser.parse_args()

    # Initialize components
    chunker = BookContentChunker(chunk_size=500, overlap=50)
    embedder = BookEmbedder(collection_name=args.collection_name)

    try:
        # Create collection, with robust error handling in the constructor
        await embedder.create_collection()

        # Find all markdown files as deep as needed
        book_path = Path(args.book_path)
        md_files = get_all_markdown_files_recursively(book_path)
        logger.info(f"Found {len(md_files)} markdown files (.md and .mdx) recursively in all subdirectories")

        # Process each file
        all_chunks = []
        for md_file in md_files:
            logger.info(f"Processing: {md_file}")

            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = chunker.chunk_markdown(content, str(md_file))
            all_chunks.extend(chunks)
            logger.info(f"  -> Generated {len(chunks)} chunks")

        logger.info(f"Total chunks: {len(all_chunks)}")

        # Upload to Qdrant
        await embedder.upload_chunks(all_chunks, doc_version=args.doc_version)

        logger.info("✅ Embedding complete!")

    finally:
        await embedder.close()


if __name__ == "__main__":
    # Run main in asyncio loop, but trap connection errors globally as a last resort
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"FATAL: Exception occurred: {type(e).__name__}: {e}")
        logger.error("Please check if Qdrant is running, accessible, and credentials are set correctly.")
        import sys
        sys.exit(1)
