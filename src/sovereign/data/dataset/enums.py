from enum import Enum


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class SampleType(str, Enum):
    QA = "qa"
    SUMMARY = "summary"
    CONVERSATION = "conversation"
    EXTRACTION = "extraction"
    CLASSIFICATION = "classification"
    REASONING = "reasoning"
    TOOL_CALLING = "tool_calling"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"