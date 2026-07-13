"""
Metric Registration
"""

from evaluation.metrics.registry import MetricRegistry

from evaluation.metrics.exact_match import ExactMatch
from evaluation.metrics.keyword_score import KeywordScore

registry = MetricRegistry()

registry.register(
    ExactMatch()
)

registry.register(
    KeywordScore()
)

__all__ = [

    "registry",

    "ExactMatch",

    "KeywordScore",

]