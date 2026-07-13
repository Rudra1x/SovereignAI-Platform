"""
Latency Metric
"""

from __future__ import annotations

from statistics import mean
from statistics import median


class LatencyMetrics:

    @staticmethod
    def summarize(
        records: list[dict],
    ) -> dict:

        latencies = [

            r["latency"]

            for r in records

        ]

        if not latencies:

            return {

                "mean": 0,

                "median": 0,

                "min": 0,

                "max": 0,

            }

        return {

            "mean": mean(latencies),

            "median": median(latencies),

            "min": min(latencies),

            "max": max(latencies),

        }