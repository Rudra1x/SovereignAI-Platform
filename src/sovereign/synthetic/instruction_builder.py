"""
Instruction dataset builder.

Converts document chunks into supervised instruction
examples for fine-tuning.
"""

from __future__ import annotations

from dataclasses import dataclass

from sovereign.synthetic.chunker import TextChunk
from sovereign.synthetic.templates import (
    INSTRUCTION_TEMPLATES,
)


@dataclass(slots=True)
class InstructionExample:

    instruction: str

    input: str

    output: str

    template: str

    source: str

    chunk_id: int

class InstructionBuilder:

    """
    Generates instruction examples from document chunks.
    """

    def build(
        self,
        *,
        source: str,
        chunks: list[TextChunk],
    ) -> list[InstructionExample]:

        examples: list[InstructionExample] = []

        for chunk in chunks:

            for template in INSTRUCTION_TEMPLATES:

                example = InstructionExample(

                    instruction=template.instruction,

                    input=chunk.text,

                    output=chunk.text,

                    template=template.name,

                    source=source,

                    chunk_id=chunk.chunk_id,

                )

                examples.append(example)

        return examples
    
def to_record(
    example: InstructionExample,
) -> dict:

    return {

        "instruction": example.instruction,

        "input": example.input,

        "output": example.output,

        "template": example.template,

        "source": example.source,

        "chunk_id": example.chunk_id,

    }