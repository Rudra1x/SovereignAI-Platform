"""
Metric Registry

Automatically stores every metric available
to the evaluation framework.
"""

from __future__ import annotations

from typing import Iterable

from evaluation.metrics.base import BaseMetric


class MetricRegistry:

    def __init__(self):

        self._metrics: dict[str, BaseMetric] = {}

    def register(
        self,
        metric: BaseMetric,
    ) -> None:

        if metric.name in self._metrics:

            raise ValueError(
                f"Metric '{metric.name}' already registered."
            )

        self._metrics[metric.name] = metric

    def unregister(
        self,
        name: str,
    ) -> None:

        self._metrics.pop(name, None)

    def get(
        self,
        name: str,
    ) -> BaseMetric:

        return self._metrics[name]

    def names(self) -> list[str]:

        return sorted(self._metrics.keys())

    def metrics(self) -> Iterable[BaseMetric]:

        return self._metrics.values()

    def __len__(self):

        return len(self._metrics)

    def __contains__(
        self,
        item: str,
    ):

        return item in self._metrics

    def __iter__(self):

        return iter(self._metrics.values())