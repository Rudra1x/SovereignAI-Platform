"""
Exact Match metric.
"""

from __future__ import annotations


class ExactMatch:

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