"""
Metric registry.
"""

from __future__ import annotations


class MetricRegistry:

    def __init__(self):

        self._metrics = []

    def register(self, metric):

        self._metrics.append(metric)

    @property
    def metrics(self):

        return self._metrics