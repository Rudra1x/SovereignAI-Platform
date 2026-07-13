"""
BERTScore Metric

Evaluates semantic similarity between predictions and references.

This is a corpus-level metric.
"""

from __future__ import annotations

from bert_score import score

from evaluation.metrics.base import BaseCorpusMetric


class BERTScoreMetric(BaseCorpusMetric):

    @property
    def name(self) -> str:
        return "bertscore"

    @property
    def description(self) -> str:
        return "Semantic similarity using BERTScore"

    def evaluate(
        self,
        records: list[dict],
    ) -> dict:

        predictions = [
            r["model_answer"]
            for r in records
        ]

        references = [
            r["reference_answer"]
            for r in records
        ]

        precision, recall, f1 = score(
            predictions,
            references,
            lang="en",
            verbose=True,
            batch_size=16,
        )

        per_question = []

        for i in range(len(records)):

            per_question.append({

                "id": records[i]["id"],

                "precision": float(precision[i]),

                "recall": float(recall[i]),

                "f1": float(f1[i]),

            })

        return {

            "metric": self.name,

            "precision": float(precision.mean()),

            "recall": float(recall.mean()),

            "f1": float(f1.mean()),

            "per_question": per_question,

        }