"""
Metric Registration
"""

from evaluation.metrics.registry import MetricRegistry

from evaluation.metrics.exact_match import ExactMatch
from evaluation.metrics.keyword_score import KeywordScore

registry = MetricRegistry()

registry.register_record(
    ExactMatch()
)

registry.register_record(
    KeywordScore()
)
from evaluation.metrics.bleu import BleuMetric
from evaluation.metrics.rouge import RougeMetric
from evaluation.metrics.bertscore import BERTScoreMetric

registry.register_corpus(
    BleuMetric()
)

registry.register_corpus(
    RougeMetric()
)

registry.register_corpus(
    BERTScoreMetric()
)