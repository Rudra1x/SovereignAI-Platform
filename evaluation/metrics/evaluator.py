"""
Evaluation engine.

Aggregates all metrics into a single report.
"""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict

from evaluation.utils import load_json
from evaluation.metrics import (
    ExactMatch,
    KeywordScore,
    LatencyMetrics,
)


class Evaluator:

    def __init__(self):

        self.exact_match = ExactMatch()
        self.keyword_score = KeywordScore()

    def evaluate(
        self,
        prediction_file: str | Path,
    ) -> dict:

        predictions = load_json(prediction_file)

        overall = {

            "questions": len(predictions),

            "exact_match": [],

            "keyword_score": [],

            "latency": [],
        }

        category_scores = defaultdict(
            lambda: {
                "questions": 0,
                "exact_match": [],
                "keyword_score": [],
            }
        )

        for item in predictions:

            exact = self.exact_match.score(
                prediction=item["model_answer"],
                reference=item["reference_answer"],
            )

            keyword = self.keyword_score.score(
                prediction=item["model_answer"],
                keywords=item.get("keywords", []),
            )

            latency = item["latency"]

            overall["exact_match"].append(exact)
            overall["keyword_score"].append(keyword)
            overall["latency"].append(latency)

            category = item["category"]

            category_scores[category]["questions"] += 1
            category_scores[category]["exact_match"].append(exact)
            category_scores[category]["keyword_score"].append(keyword)

        report = {

            "overall": {

                "questions": overall["questions"],

                "exact_match":

                    sum(overall["exact_match"])
                    / max(1, len(overall["exact_match"])),

                "keyword_score":

                    sum(overall["keyword_score"])
                    / max(1, len(overall["keyword_score"])),

                "latency":

                    LatencyMetrics.summarize(
                        overall["latency"]
                    ),
            },

            "categories": {},
        }

        for category, values in category_scores.items():

            report["categories"][category] = {

                "questions": values["questions"],

                "exact_match":

                    sum(values["exact_match"])
                    / max(1, len(values["exact_match"])),

                "keyword_score":

                    sum(values["keyword_score"])
                    / max(1, len(values["keyword_score"])),

            }

        return report