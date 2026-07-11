"""
Hallucination plugin.
"""

from __future__ import annotations

from evaluation.plugins.base import EvaluationPlugin

from evaluation.hallucination import HallucinationDetector


class HallucinationPlugin(EvaluationPlugin):

    name = "hallucination"

    def __init__(self):

        self.detector = HallucinationDetector()

    def supports(
        self,
        sample,
    ):

        return True

    def evaluate(
        self,
        sample,
        prediction,
    ):

        hallucinations = (

            self.detector.api_hallucination(

                prediction["model_answer"]

            )

        )

        return {

            "hallucinations":

                hallucinations,

            "count":

                len(hallucinations),

        }