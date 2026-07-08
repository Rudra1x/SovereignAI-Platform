from __future__ import annotations

from abc import ABC, abstractmethod

from sovereign.data.dataset.record import CanonicalRecord
from sovereign.data.extraction.unit import KnowledgeUnit


class BaseGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        unit: KnowledgeUnit,
    ) -> list[CanonicalRecord]:
        raise NotImplementedError