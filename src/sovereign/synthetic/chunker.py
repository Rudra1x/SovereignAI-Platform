"""
Semantic Document Chunker

Splits canonical documents into semantically meaningful chunks
for synthetic instruction generation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# ---------------------------------------------------------------------
# Chunk Object
# ---------------------------------------------------------------------


@dataclass(slots=True)
class TextChunk:

    chunk_id: int

    document_id: str

    title: str

    source: str

    section: str

    text: str

    word_count: int

    character_count: int


# ---------------------------------------------------------------------
# Semantic Chunker
# ---------------------------------------------------------------------


class SemanticChunker:

    def __init__(
        self,
        chunk_size: int = 700,
        overlap: int = 100,
        min_chunk_size: int = 150,
    ):

        if overlap >= chunk_size:

            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size

        self.overlap = overlap

        self.min_chunk_size = min_chunk_size

    # -------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------

    @staticmethod
    def word_count(text: str) -> int:

        return len(text.split())

    @staticmethod
    def normalize(text: str) -> str:

        if not text:

            return ""

        text = text.replace("\r\n", "\n")

        text = text.replace("\r", "\n")

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    # -------------------------------------------------------------
    # Paragraph Split
    # -------------------------------------------------------------

    def split_paragraphs(
        self,
        text: str,
    ) -> list[str]:

        text = self.normalize(text)

        paragraphs = []

        for paragraph in text.split("\n\n"):

            paragraph = paragraph.strip()

            if paragraph:

                paragraphs.append(paragraph)

        return paragraphs

    # -------------------------------------------------------------
    # Section Detection
    # -------------------------------------------------------------

    @staticmethod
    def detect_section(
        paragraph: str,
    ) -> str:

        lines = paragraph.splitlines()

        if not lines:

            return ""

        first = lines[0].strip()

        if first.startswith("#"):

            return first.lstrip("#").strip()

        return ""

    # -------------------------------------------------------------
    # Merge Small Paragraphs
    # -------------------------------------------------------------

    def merge_small_paragraphs(
        self,
        paragraphs: list[str],
    ) -> list[str]:

        merged = []

        buffer = ""

        for paragraph in paragraphs:

            if not buffer:

                buffer = paragraph

                continue

            current_words = self.word_count(buffer)

            next_words = self.word_count(paragraph)

            if (
                current_words < self.min_chunk_size
                or next_words < self.min_chunk_size
            ):

                buffer += "\n\n" + paragraph

            else:

                merged.append(buffer)

                buffer = paragraph

        if buffer:

            merged.append(buffer)

        return merged
        # -------------------------------------------------------------
    # Build Chunks
    # -------------------------------------------------------------

    def build_chunks(
        self,
        paragraphs: list[str],
        document_id: str,
        title: str,
        source: str,
    ) -> list[TextChunk]:

        chunks: list[TextChunk] = []

        current_paragraphs: list[str] = []

        current_section = ""

        chunk_id = 0

        for paragraph in paragraphs:

            section = self.detect_section(paragraph)

            if section:

                current_section = section

            candidate = current_paragraphs + [paragraph]

            candidate_text = "\n\n".join(candidate)

            candidate_words = self.word_count(candidate_text)

            if (
                candidate_words <= self.chunk_size
                or not current_paragraphs
            ):

                current_paragraphs.append(paragraph)

                continue

            chunk_text = "\n\n".join(current_paragraphs)

            chunks.append(

                TextChunk(

                    chunk_id=chunk_id,

                    document_id=document_id,

                    title=title,

                    source=source,

                    section=current_section,

                    text=chunk_text,

                    word_count=self.word_count(chunk_text),

                    character_count=len(chunk_text),

                )

            )

            chunk_id += 1

            overlap_paragraphs = self.compute_overlap(
                current_paragraphs
            )

            current_paragraphs = (
                overlap_paragraphs + [paragraph]
            )

        if current_paragraphs:

            chunk_text = "\n\n".join(current_paragraphs)

            chunks.append(

                TextChunk(

                    chunk_id=chunk_id,

                    document_id=document_id,

                    title=title,

                    source=source,

                    section=current_section,

                    text=chunk_text,

                    word_count=self.word_count(chunk_text),

                    character_count=len(chunk_text),

                )

            )

        return chunks

    # -------------------------------------------------------------
    # Overlap Builder
    # -------------------------------------------------------------

    def compute_overlap(
        self,
        paragraphs: list[str],
    ) -> list[str]:

        if not paragraphs:

            return []

        overlap: list[str] = []

        total_words = 0

        for paragraph in reversed(paragraphs):

            overlap.insert(0, paragraph)

            total_words += self.word_count(paragraph)

            if total_words >= self.overlap:

                break

        return overlap

    # -------------------------------------------------------------
    # Chunk Statistics
    # -------------------------------------------------------------

    @staticmethod
    def statistics(
        chunks: list[TextChunk],
    ) -> dict:

        if not chunks:

            return {

                "chunks": 0,

                "words": 0,

                "average_words": 0,

            }

        total_words = sum(

            chunk.word_count

            for chunk in chunks

        )

        return {

            "chunks": len(chunks),

            "words": total_words,

            "average_words": round(

                total_words / len(chunks),

                2,

            ),

        }
    
        # -------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------

    def validate_chunk(
        self,
        chunk: TextChunk,
    ) -> bool:

        if not chunk.text.strip():
            return False

        if chunk.word_count <= 0:
            return False

        if chunk.character_count <= 0:
            return False

        return True

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------

    def chunk_document(
        self,
        document: dict,
    ) -> list[TextChunk]:

        paragraphs = self.split_paragraphs(
            document["text"]
        )

        paragraphs = self.merge_small_paragraphs(
            paragraphs
        )

        chunks = self.build_chunks(
            paragraphs=paragraphs,
            document_id=document["id"],
            title=document["title"],
            source=document["source"],
        )

        return [
            chunk
            for chunk in chunks
            if self.validate_chunk(chunk)
        ]

    # -------------------------------------------------------------
    # Convenience API
    # -------------------------------------------------------------

    def __call__(
        self,
        document: dict,
    ) -> list[TextChunk]:

        return self.chunk_document(document)