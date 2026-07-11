"""
Base evaluation plugin.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EvaluationPlugin(ABC):

    name = "base"

    @abstractmethod
    def supports(
        self,
        sample: dict,
    ) -> bool:
        ...

    @abstractmethod
    def evaluate(
        self,
        sample: dict,
        prediction: dict,
    ) -> dict:
        ...