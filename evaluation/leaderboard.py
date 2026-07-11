"""
Model Leaderboard
"""

from __future__ import annotations


class Leaderboard:

    def compare(
        self,
        base,
        adapter,
        merged,
    ):

        return {

            "Exact Match": {

                "Base": base["exact_match"],

                "Adapter": adapter["exact_match"],

                "Merged": merged["exact_match"],
            },

            "BLEU": {

                "Base": base["bleu"],

                "Adapter": adapter["bleu"],

                "Merged": merged["bleu"],
            },

            "BERTScore": {

                "Base": base["bertscore"],

                "Adapter": adapter["bertscore"],

                "Merged": merged["bertscore"],
            },
        }