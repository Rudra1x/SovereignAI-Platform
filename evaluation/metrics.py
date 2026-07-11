"""
Evaluation metrics for SovereignAI.
"""

from __future__ import annotations

from bert_score import score
from rouge_score import rouge_scorer
from sacrebleu.metrics import BLEU


class Metrics:

    def __init__(self):

        self.bleu = BLEU()

        self.rouge = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"],
            use_stemmer=True,
        )

    def exact_match(
        self,
        prediction,
        reference,
    ):

        return (
            prediction.strip().lower()
            ==
            reference.strip().lower()
        )

    def keyword_recall(
        self,
        prediction,
        keywords,
    ):

        prediction = prediction.lower()

        hits = sum(
            keyword.lower() in prediction
            for keyword in keywords
        )

        if len(keywords) == 0:
            return 0.0

        return hits / len(keywords)

    def bleu_score(
        self,
        prediction,
        reference,
    ):

        return self.bleu.sentence_score(
            prediction,
            [reference],
        ).score

    def rouge_scores(
        self,
        prediction,
        reference,
    ):

        scores = self.rouge.score(
            reference,
            prediction,
        )

        return {
            "rouge1": scores["rouge1"].fmeasure,
            "rouge2": scores["rouge2"].fmeasure,
            "rougeL": scores["rougeL"].fmeasure,
        }

    def bert_score(
        self,
        prediction,
        reference,
    ):

        P, R, F = score(
            [prediction],
            [reference],
            lang="en",
            verbose=False,
        )

        return float(F.mean())