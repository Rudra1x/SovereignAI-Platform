"""
Coding plugin.
"""

from __future__ import annotations

from evaluation.plugins.base import EvaluationPlugin

from evaluation.code_evaluator import CodeEvaluator


class CodingPlugin(EvaluationPlugin):

    name = "coding"

    def __init__(self):

        self.executor = CodeEvaluator()

    def supports(
        self,
        sample,
    ):

        return sample["task"] in {

            "coding",

            "debugging",

        }

    def evaluate(
        self,
        sample,
        prediction,
    ):

        code = self.executor.extract_python(

            prediction["model_answer"]

        )

        result = self.executor.execute(

            code

        )

        return result