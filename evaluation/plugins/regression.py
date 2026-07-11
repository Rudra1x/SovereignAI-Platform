"""
Regression plugin.
"""

from __future__ import annotations

from evaluation.plugins.base import EvaluationPlugin


class RegressionPlugin(EvaluationPlugin):

    name = "regression"

    def supports(
        self,
        sample,
    ):

        return sample["category"] == "General"

    def evaluate(
        self,
        sample,
        prediction,
    ):

        return {

            "checked": True

        }