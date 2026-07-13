"""
Exact Match metric.
"""
from evaluation.metrics.base import BaseMetric
from __future__ import annotations


class ExactMatch:

    @property
    def name(self):

        return "exact_match"

    @staticmethod
    def normalize(text: str) -> str:

        if text is None:
            return ""

        return (
            text.strip()
            .lower()
            .replace(".", "")
            .replace(",", "")
            .replace("\n", " ")
        )

    @classmethod
    def score(
        cls,
        prediction: str,
        reference: str,
    ) -> float:

        prediction = cls.normalize(prediction)
        reference = cls.normalize(reference)

        return float(prediction == reference)
    
class KeywordScore(BaseMetric):

    @property
    def name(self):

        return "keyword_score"