"""
Document chunking utilities.

Converts canonical documents into training chunks suitable
for instruction tuning.

The implementation is intentionally simple and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TextChunk:

    chunk_id: int

    text: str

    word_count: int


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 300,
        overlap: int = 50,
    ):

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
    ) -> list[TextChunk]:

        if not text.strip():
            return []

        words = text.split()

        chunks: list[TextChunk] = []

        step = self.chunk_size - self.overlap

        chunk_id = 0

        for start in range(0, len(words), step):

            end = start + self.chunk_size

            chunk_words = words[start:end]

            if not chunk_words:
                break

            chunk_text = " ".join(chunk_words)

            chunks.append(

                TextChunk(

                    chunk_id=chunk_id,

                    text=chunk_text,

                    word_count=len(chunk_words),

                )

            )

            chunk_id += 1

            if end >= len(words):
                break

        return chunks