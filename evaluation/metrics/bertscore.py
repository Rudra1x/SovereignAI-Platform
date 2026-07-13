"""
BERTScore metric.
"""

from __future__ import annotations

from bert_score import score

from evaluation.metrics.base import BaseMetric


class BERTScoreMetric(BaseMetric):

    @property
    def name(self):

        return "bertscore"

    def score(
        self,
        prediction: str,
        reference: str,
        metadata: dict,
    ) -> float:

        _, _, f1 = score(

            [prediction],

            [reference],

            lang="en",

            verbose=False,

        )

        return float(f1[0])