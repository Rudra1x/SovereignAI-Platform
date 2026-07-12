"""
Chart generation for evaluation reports.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


class ChartGenerator:

    @staticmethod
    def latency_chart(report: dict, output_dir: str | Path):

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        latency = report["overall"]["latency"]

        labels = ["Mean", "Median", "Min", "Max"]

        values = [
            latency["mean"],
            latency["median"],
            latency["min"],
            latency["max"],
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values)

        plt.ylabel("Seconds")

        plt.title("Latency Summary")

        plt.tight_layout()

        plt.savefig(
            output_dir / "latency.png",
            dpi=300,
        )

        plt.close()

    @staticmethod
    def category_chart(report: dict, output_dir: str | Path):

        output_dir = Path(output_dir)

        categories = []
        scores = []

        for category, result in report["categories"].items():

            categories.append(category)

            scores.append(
                result["keyword_score"]
            )

        plt.figure(figsize=(10, 6))

        plt.barh(categories, scores)

        plt.xlim(0, 1)

        plt.xlabel("Keyword Score")

        plt.title("Category Performance")

        plt.tight_layout()

        plt.savefig(
            output_dir / "category_scores.png",
            dpi=300,
        )

        plt.close()

    @staticmethod
    def overall_chart(report: dict, output_dir: str | Path):

        output_dir = Path(output_dir)

        metrics = [
            "Exact Match",
            "Keyword Score",
        ]

        values = [

            report["overall"]["exact_match"],

            report["overall"]["keyword_score"],

        ]

        plt.figure(figsize=(6, 5))

        plt.bar(metrics, values)

        plt.ylim(0, 1)

        plt.ylabel("Score")

        plt.title("Overall Metrics")

        plt.tight_layout()

        plt.savefig(
            output_dir / "overall_metrics.png",
            dpi=300,
        )

        plt.close()

    @classmethod
    def generate_all(
        cls,
        report,
        output_dir,
    ):

        cls.latency_chart(
            report,
            output_dir,
        )

        cls.category_chart(
            report,
            output_dir,
        )

        cls.overall_chart(
            report,
            output_dir,
        )