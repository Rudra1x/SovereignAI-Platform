"""
Statistical Analysis
"""

from collections import defaultdict


class StatisticalAnalyzer:

    def category_scores(
        self,
        results,
    ):

        scores = defaultdict(list)

        for sample in results:

            scores[
                sample["category"]
            ].append(

                sample["metrics"]["bertscore"]

            )

        averages = {}

        for category in scores:

            averages[category] = (

                sum(scores[category])

                /

                len(scores[category])

            )

        return averages