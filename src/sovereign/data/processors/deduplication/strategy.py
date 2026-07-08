from abc import ABC, abstractmethod


class DeduplicationStrategy(ABC):

    @abstractmethod
    def score(
        self,
        text: str,
    ) -> float:
        pass