"""
Instruction templates.

These templates are used to generate supervised instruction
examples from the canonical corpus.

The templates are intentionally domain-agnostic so the same
pipeline can be reused for future clients by simply changing
the corpus.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstructionTemplate:

    name: str

    instruction: str


INSTRUCTION_TEMPLATES: list[InstructionTemplate] = [

    InstructionTemplate(
        name="explain",
        instruction="Explain the following concept in a clear and detailed manner."
    ),

    InstructionTemplate(
        name="summary",
        instruction="Write a concise summary of the following document."
    ),

    InstructionTemplate(
        name="key_points",
        instruction="Extract the key points from the following document."
    ),

    InstructionTemplate(
        name="definition",
        instruction="Define the important concepts mentioned in the following document."
    ),

    InstructionTemplate(
        name="tutorial",
        instruction="Teach the following topic step by step for a beginner."
    ),

    InstructionTemplate(
        name="technical",
        instruction="Provide a technical explanation of the following content."
    ),

    InstructionTemplate(
        name="implementation",
        instruction="Explain how this concept can be implemented in practice."
    ),

    InstructionTemplate(
        name="best_practices",
        instruction="List the best practices described in the following content."
    ),

    InstructionTemplate(
        name="advantages",
        instruction="Explain the advantages and limitations discussed in the following content."
    ),

    InstructionTemplate(
        name="faq",
        instruction="Generate frequently asked questions and answers from the following content."
    ),
]