"""
Keyword Coverage Metric
"""

from __future__ import annotations

from evaluation.metrics.base import BaseMetric
from evaluation.metrics.base import BaseRecordMetric

class KeywordScore(BaseRecordMetric):

    @property
    def name(self):

        return "keyword_score"

    @property
    def description(self):

        return "Keyword Coverage"

    def score(
        self,
        record: dict,
    ) -> dict:

        prediction = record["model_answer"].lower()

        keywords = [

            k.lower()

            for k in record.get(

                "keywords",

                [],

            )

        ]

        if not keywords:

            return {

                "metric": self.name,

                "score": 1.0,

                "hits": [],

                "missing": [],

            }

        hits = []

        missing = []

        for keyword in keywords:

            if keyword in prediction:

                hits.append(keyword)

            else:

                missing.append(keyword)

        score = len(hits) / len(keywords)

        return {

            "metric": self.name,

            "score": score,

            "hits": hits,

            "missing": missing,

        }