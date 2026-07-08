from abc import ABC, abstractmethod


class QualityStrategy(ABC):

    @abstractmethod
    def score(
        self,
        text: str,
    ) -> float:
        pass