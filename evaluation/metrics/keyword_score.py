"""
Keyword coverage metric.
"""

from __future__ import annotations


class KeywordScore:

    @staticmethod
    def score(
        prediction: str,
        keywords: list[str],
    ) -> float:

        if not keywords:
            return 1.0

        prediction = prediction.lower()

        hits = 0

        for keyword in keywords:

            if keyword.lower() in prediction:

                hits += 1

        return hits / len(keywords)