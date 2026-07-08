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


class QAGenerator(BaseGenerator):

    def generate(self, unit):

        conversation = Conversation()

        conversation.add(
            Message(
                role=Role.USER,
                content=f"Explain the following concept:\n\n{unit.text}"
            )
        )

        conversation.add(
            Message(
                role=Role.ASSISTANT,
                content=unit.text
            )
        )

        record = CanonicalRecord(
            conversation=conversation,
            metadata=DatasetMetadata(
                source_document=unit.source_document,
            ),
            sample_type=SampleType.QA,
            difficulty=Difficulty.MEDIUM,
            score=1.0,
        )

        return [record]