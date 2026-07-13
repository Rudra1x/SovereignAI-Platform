"""
ROUGE-L Metric
"""

from __future__ import annotations

from rouge_score import rouge_scorer

from evaluation.metrics.base import BaseCorpusMetric


class RougeMetric(BaseCorpusMetric):

    def __init__(self):

        self.scorer = rouge_scorer.RougeScorer(

            ["rougeL"],

            use_stemmer=True,

        )

    @property
    def name(self):

        return "rouge"

    @property
    def description(self):

        return "ROUGE-L"

    def evaluate(
        self,
        records,
    ):

        scores = []

        for record in records:

            result = self.scorer.score(

                record["reference_answer"],

                record["model_answer"],

            )

            scores.append(

                result["rougeL"].fmeasure

            )

        return {

            "metric": self.name,

            "score": sum(scores) / len(scores),

            "per_question": scores,

        }