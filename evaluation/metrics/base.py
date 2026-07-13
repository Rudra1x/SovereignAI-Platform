"""
Base class for all evaluation metrics.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseMetric(ABC):
    """
    Base class that every metric must inherit.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Metric name.
        """
        pass

    @abstractmethod
    def score(
        self,
        prediction: str,
        reference: str,
        metadata: dict,
    ):
        """
        Calculate the metric.

        Returns either:
        - float
        - dict
        """
        pass