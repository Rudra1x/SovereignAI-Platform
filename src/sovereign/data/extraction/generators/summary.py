from sovereign.data.dataset import (
    CanonicalRecord,
    Conversation,
    DatasetMetadata,
    Difficulty,
    Message,
    Role,
    SampleType,
)

from sovereign.data.extraction.generators.base import BaseGenerator


class SummaryGenerator(BaseGenerator):

    def generate(self, unit):

        conversation = Conversation()

        conversation.add(
            Message(
                role=Role.USER,
                content="Summarize the following text."
            )
        )

        conversation.add(
            Message(
                role=Role.ASSISTANT,
                content=unit.text
            )
        )

        return [
            CanonicalRecord(
                conversation=conversation,
                metadata=DatasetMetadata(
                    source_document=unit.source_document,
                ),
                sample_type=SampleType.SUMMARY,
            )
        ]