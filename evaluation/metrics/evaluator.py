"""
Evaluation Engine

Runs every registered metric on every prediction and
produces an aggregated evaluation report.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any

from evaluation.metrics import registry
from evaluation.metrics.latency import LatencyMetrics


class Evaluator:
    """
    Main evaluation engine.
    """

    def __init__(self):

        self.registry = registry

    def evaluate(
        self,
        predictions: list[dict[str, Any]],
    ) -> dict[str, Any]:

        report = {

            "overall": {},

            "categories": {},

            "questions": [],
        }

        metric_scores = defaultdict(list)

        category_scores = defaultdict(
            lambda: defaultdict(list)
        )

        # ----------------------------------------------------
        # Evaluate every prediction
        # ----------------------------------------------------

        for record in predictions:

            question_result = {

                "id": record.get("id"),

                "category": record.get("category"),

                "difficulty": record.get("difficulty"),

                "metrics": {},

            }

            for metric in self.registry:

                result = metric.score(record)

                question_result["metrics"][
                    metric.name
                ] = result

                if "score" in result:

                    metric_scores[
                        metric.name
                    ].append(
                        result["score"]
                    )

                    category_scores[
                        record["category"]
                    ][
                        metric.name
                    ].append(
                        result["score"]
                    )

            report["questions"].append(
                question_result
            )

        # ----------------------------------------------------
        # Overall Scores
        # ----------------------------------------------------

        for metric_name, values in metric_scores.items():

            report["overall"][metric_name] = {

                "mean": mean(values),

                "count": len(values),

            }

        # ----------------------------------------------------
        # Category Scores
        # ----------------------------------------------------

        for category in category_scores:

            report["categories"][category] = {}

            for metric_name, values in category_scores[
                category
            ].items():

                report["categories"][
                    category
                ][metric_name] = {

                    "mean": mean(values),

                    "count": len(values),

                }

        # ----------------------------------------------------
        # Latency
        # ----------------------------------------------------

        report["overall"][
            "latency"
        ] = LatencyMetrics.summarize(
            predictions
        )

        return report