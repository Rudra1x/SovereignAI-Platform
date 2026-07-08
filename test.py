from sovereign.data.dataset import *

conversation = Conversation()

conversation.add(
    Message(
        role=Role.USER,
        content="What is a qubit?"
    )
)

conversation.add(
    Message(
        role=Role.ASSISTANT,
        content="A qubit is the basic unit of quantum information."
    )
)

record = CanonicalRecord(
    conversation=conversation,
    metadata=DatasetMetadata(
        source_document="README.md",
        language="en",
        quality_score=0.95
    ),
    sample_type=SampleType.QA
)

print(record)