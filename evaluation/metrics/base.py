"""
Base classes for the evaluation framework.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseMetric(ABC):
    """
    Common functionality for every metric.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        return self.name


class BaseRecordMetric(BaseMetric):
    """
    Metric evaluated on one prediction record.
    """

    @abstractmethod
    def score(
        self,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        ...


class BaseCorpusMetric(BaseMetric):
    """
    Metric evaluated on the complete benchmark.
    """

    @abstractmethod
    def evaluate(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        ...