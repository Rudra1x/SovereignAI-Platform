"""
Reasoning plugin.
"""

from __future__ import annotations

from evaluation.plugins.base import EvaluationPlugin


class ReasoningPlugin(EvaluationPlugin):

    name = "reasoning"

    def supports(
        self,
        sample,
    ):

        return sample["task"] in {

            "reasoning",

            "comparison",

        }

    def evaluate(
        self,
        sample,
        prediction,
    ):

        answer = prediction["model_answer"]

        sentences = [

            s

            for s in answer.split(".")

            if s.strip()

        ]

        return {

            "reasoning_steps":

                len(sentences)

        }