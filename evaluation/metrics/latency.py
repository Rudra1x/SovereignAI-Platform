"""
Latency metrics.
"""

from __future__ import annotations

from statistics import mean
from statistics import median


class LatencyMetrics:

    @staticmethod
    def summarize(
        values: list[float],
    ) -> dict:

        if not values:

            return {
                "mean": 0,
                "median": 0,
                "min": 0,
                "max": 0,
            }

        return {

            "mean": mean(values),

            "median": median(values),

            "min": min(values),

            "max": max(values),

        }