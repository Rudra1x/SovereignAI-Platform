"""
ROUGE-L metric.
"""

from __future__ import annotations

from rouge_score import rouge_scorer

from evaluation.metrics.base import BaseMetric


class RougeScore(BaseMetric):

    def __init__(self):

        self.scorer = rouge_scorer.RougeScorer(

            ["rougeL"],

            use_stemmer=True,

        )

    @property
    def name(self):

        return "rouge"

    def score(
        self,
        prediction: str,
        reference: str,
        metadata: dict,
    ) -> float:

        score = self.scorer.score(

            reference,

            prediction,

        )

        return score["rougeL"].fmeasure