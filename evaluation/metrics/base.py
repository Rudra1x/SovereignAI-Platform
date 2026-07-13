"""
Base Metric Interface

Every evaluation metric in the framework must inherit from BaseMetric.

The metric receives a complete prediction record and returns
a structured dictionary describing the evaluation result.

Author:
    QuantumQwen Evaluation Framework
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseMetric(ABC):
    """
    Base class for every evaluation metric.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique metric name.

        Example:
            bertscore
            rouge
            bleu
            keyword_score
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        Human-readable description.
        """

        return self.__class__.__name__

    @abstractmethod
    def score(
        self,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Evaluate a single prediction.

        Parameters
        ----------
        record

            Prediction dictionary.

            Example

            {
                "id": 17,
                "question": "...",
                "reference_answer": "...",
                "model_answer": "...",
                "keywords": [...],
                "latency": 4.82,
                "category": "...",
                "difficulty": "..."
            }

        Returns
        -------

        Dictionary.

        Example

        {
            "metric": "keyword_score",
            "score": 0.83
        }
        """
        raise NotImplementedError

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}(name='{self.name}')"