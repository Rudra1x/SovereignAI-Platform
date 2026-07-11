"""
Evaluates prediction files.
"""

from __future__ import annotations

from evaluation.metrics import Metrics
from evaluation.utils import load_json


class Evaluator:

    def __init__(self):

        self.metrics = Metrics()

    def evaluate(
        self,
        prediction_file,
    ):

        predictions = load_json(
            prediction_file
        )

        results = []

        for sample in predictions:

            metrics = {

                "exact_match":

                    self.metrics.exact_match(
                        sample["model_answer"],
                        sample["reference_answer"],
                    ),

                "keyword_recall":

                    self.metrics.keyword_recall(
                        sample["model_answer"],
                        sample["keywords"],
                    ),

                "bleu":

                    self.metrics.bleu_score(
                        sample["model_answer"],
                        sample["reference_answer"],
                    ),

                "rouge":

                    self.metrics.rouge_scores(
                        sample["model_answer"],
                        sample["reference_answer"],
                    ),

                "bertscore":

                    self.metrics.bert_score(
                        sample["model_answer"],
                        sample["reference_answer"],
                    ),
            }

            sample["metrics"] = metrics

            results.append(sample)

        return results