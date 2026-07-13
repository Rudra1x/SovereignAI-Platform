"""
BLEU metric.
"""

from __future__ import annotations

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

from evaluation.metrics.base import BaseMetric


class BleuScore(BaseMetric):

    @property
    def name(self):

        return "bleu"

    def score(
        self,
        prediction: str,
        reference: str,
        metadata: dict,
    ) -> float:

        smoothie = SmoothingFunction().method4

        return sentence_bleu(

            [reference.split()],

            prediction.split(),

            smoothing_function=smoothie,

        )