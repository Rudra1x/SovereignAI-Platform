"""
Production Evaluation Engine

Runs all registered metrics and returns a canonical report.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean

from evaluation.metrics import registry
from evaluation.metrics.latency import LatencyMetrics


class Evaluator:

    def __init__(self):

        self.registry = registry

    def evaluate(
        self,
        predictions: list[dict],
    ) -> dict:

        report = {

            "metadata": {},

            "overall": {},

            "categories": {},

            "questions": [],

        }

        metric_scores = defaultdict(list)

        category_scores = defaultdict(
            lambda: defaultdict(list)
        )

        # --------------------------------------------------
        # Record Metrics
        # --------------------------------------------------

        for record in predictions:

            result = {

                "id": record.get("id"),

                "category": record.get(
                    "category",
                    "Unknown",
                ),

                "difficulty": record.get(
                    "difficulty",
                    "Unknown",
                ),

                "question": record.get(
                    "question",
                    "",
                ),

                "metrics": {},

            }

            for metric in self.registry.record_metrics:

                metric_result = metric.score(
                    record
                )

                result["metrics"][
                    metric.name
                ] = metric_result

                if "score" in metric_result:

                    value = metric_result["score"]

                    metric_scores[
                        metric.name
                    ].append(value)

                    category_scores[
                        result["category"]
                    ][
                        metric.name
                    ].append(value)

            report["questions"].append(
                result
            )

        # --------------------------------------------------
        # Aggregate Record Metrics
        # --------------------------------------------------

        for metric_name, values in metric_scores.items():

            report["overall"][
                metric_name
            ] = {

                "mean": mean(values),

                "count": len(values),

            }

        # --------------------------------------------------
        # Category Metrics
        # --------------------------------------------------

        for category in category_scores:

            report["categories"][
                category
            ] = {}

            for metric_name, values in category_scores[
                category
            ].items():

                report["categories"][
                    category
                ][
                    metric_name
                ] = {

                    "mean": mean(values),

                    "count": len(values),

                }

        # --------------------------------------------------
        # Corpus Metrics
        # --------------------------------------------------

        for metric in self.registry.corpus_metrics:

            report["overall"][
                metric.name
            ] = metric.evaluate(
                predictions
            )

        # --------------------------------------------------
        # Latency
        # --------------------------------------------------

        report["overall"][
            "latency"
        ] = LatencyMetrics.summarize(
            predictions
        )

        return report