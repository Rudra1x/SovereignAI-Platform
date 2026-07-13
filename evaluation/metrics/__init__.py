from evaluation.metrics.exact_match import ExactMatch
from evaluation.metrics.keyword_score import KeywordScore
from evaluation.metrics.latency import LatencyMetrics
from evaluation.metrics.registry import MetricRegistry
from evaluation.metrics.base import BaseMetric
from evaluation.metrics.registry import MetricRegistry

from evaluation.metrics.exact_match import ExactMatch
from evaluation.metrics.keyword_score import KeywordScore
from evaluation.metrics.bleu import BleuScore
from evaluation.metrics.rouge import RougeScore
from evaluation.metrics.bertscore import BERTScoreMetric

registry = MetricRegistry()

registry.register(ExactMatch())
registry.register(KeywordScore())
registry.register(BleuScore())
registry.register(RougeScore())
registry.register(BERTScoreMetric())
from evaluation.metrics.exact_match import ExactMatch
from evaluation.metrics.keyword_score import KeywordScore
from evaluation.metrics.latency import LatencyMetrics
__all__ = [
    "ExactMatch",
    "KeywordScore",
    "LatencyMetrics",
    "MetricRegistry",
    "BaseMetric"
]