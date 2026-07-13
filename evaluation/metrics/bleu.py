"""
BLEU Metric
"""

from __future__ import annotations

import sacrebleu

from evaluation.metrics.base import BaseCorpusMetric


class BleuMetric(BaseCorpusMetric):

    @property
    def name(self):

        return "bleu"

    @property
    def description(self):

        return "Corpus BLEU"

    def evaluate(
        self,
        records,
    ):

        predictions = []

        references = []

        for record in records:

            predictions.append(

                record["model_answer"]

            )

            references.append(

                record["reference_answer"]

            )

        bleu = sacrebleu.corpus_bleu(

            predictions,

            [references],

        )

        return {

            "metric": self.name,

            "score": bleu.score,

        }