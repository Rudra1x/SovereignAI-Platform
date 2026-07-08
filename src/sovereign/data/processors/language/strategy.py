from __future__ import annotations

from abc import ABC, abstractmethod


class LanguageStrategy(ABC):

    @abstractmethod
    def detect(self, text: str) -> str:
        pass