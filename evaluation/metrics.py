"""
Evaluation Metrics
"""

from __future__ import annotations


class Metrics:

    @staticmethod
    def exact_match(
        prediction,
        reference,
    ):

        return (
            prediction.strip().lower()
            ==
            reference.strip().lower()
        )

    @staticmethod
    def keyword_recall(
        prediction,
        keywords,
    ):

        prediction = prediction.lower()

        hits = 0

        for word in keywords:

            if word.lower() in prediction:

                hits += 1

        if len(keywords) == 0:

            return 0.0

        return hits / len(keywords)