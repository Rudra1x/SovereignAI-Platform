from dataclasses import dataclass, field

from .message import Message


@dataclass(slots=True)
class Conversation:

    messages: list[Message] = field(default_factory=list)

    def add(self, message: Message):

        self.messages.append(message)

        return self