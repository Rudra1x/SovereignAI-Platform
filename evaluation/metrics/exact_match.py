"""
Exact Match Metric

Useful for:

- MCQ
- True / False
- One-word answers
- Short factual answers
"""

from __future__ import annotations

import re

from evaluation.metrics.base import BaseMetric


class ExactMatch(BaseMetric):

    @property
    def name(self) -> str:

        return "exact_match"

    @property
    def description(self) -> str:

        return "Exact string match"

    @staticmethod
    def normalize(text: str) -> str:

        if text is None:
            return ""

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        return text

    def score(
        self,
        record: dict,
    ) -> dict:

        prediction = self.normalize(
            record["model_answer"]
        )

        reference = self.normalize(
            record["reference_answer"]
        )

        score = float(
            prediction == reference
        )

        return {

            "metric": self.name,

            "score": score,

            "matched": bool(score),

        }