"""
Metric registry.
"""

from __future__ import annotations

from evaluation.metrics.base import (
    BaseCorpusMetric,
    BaseRecordMetric,
)


class MetricRegistry:

    def __init__(self):

        self._record_metrics = []

        self._corpus_metrics = []

    def register_record(
        self,
        metric: BaseRecordMetric,
    ):

        self._record_metrics.append(metric)

    def register_corpus(
        self,
        metric: BaseCorpusMetric,
    ):

        self._corpus_metrics.append(metric)

    @property
    def record_metrics(self):

        return self._record_metrics

    @property
    def corpus_metrics(self):

        return self._corpus_metrics