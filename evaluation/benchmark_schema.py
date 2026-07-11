"""
Benchmark schema for evaluating LLMs.

Every benchmark question must satisfy this schema.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BenchmarkItem:

    id: int

    category: str

    difficulty: str

    task: str

    question: str

    reference_answer: Optional[str] = None

    keywords: list[str] = field(default_factory=list)

    code_language: Optional[str] = None

    metadata: dict = field(default_factory=dict)