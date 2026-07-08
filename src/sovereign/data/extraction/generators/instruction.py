from sovereign.data.dataset import (
    CanonicalRecord,
    Conversation,
    DatasetMetadata,
    Message,
    Role,
    SampleType,
)

from sovereign.data.extraction.generators.base import BaseGenerator


class InstructionGenerator(BaseGenerator):

    def generate(self, unit):

        conv = Conversation()

        conv.add(
            Message(
                role=Role.USER,
                content=f"Teach me about:\n{unit.text}"
            )
        )

        conv.add(
            Message(
                role=Role.ASSISTANT,
                content=unit.text
            )
        )

        return [
            CanonicalRecord(
                conversation=conv,
                metadata=DatasetMetadata(
                    source_document=unit.source_document
                ),
                sample_type=SampleType.CONVERSATION,
            )
        ]