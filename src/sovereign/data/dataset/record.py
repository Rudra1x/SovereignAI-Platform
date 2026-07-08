from dataclasses import dataclass

from .conversation import Conversation
from .enums import Difficulty
from .enums import SampleType
from .metadata import DatasetMetadata


@dataclass(slots=True)
class CanonicalRecord:

    conversation: Conversation

    metadata: DatasetMetadata

    sample_type: SampleType

    difficulty: Difficulty = Difficulty.MEDIUM

    score: float = 0.0