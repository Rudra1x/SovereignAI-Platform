"""
Chart Generator

Creates charts from the evaluation report.

Uses matplotlib only.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


class ChartGenerator:

    @staticmethod
    def _extract_metric(metric_value):

        if not isinstance(metric_value, dict):
            return None

        if "f1" in metric_value:
            return metric_value["f1"]

        if "score" in metric_value:
            return metric_value["score"]

        if "mean" in metric_value:
            return metric_value["mean"]

        return None

    @staticmethod
    def generate_overall_metrics(
        report: dict,
        output_dir: Path,
    ):

        overall = report.get("overall", {})

        metrics = []
        values = []

        for metric_name, metric_data in overall.items():

            value = ChartGenerator._extract_metric(
                metric_data
            )

            if value is None:
                continue

            metrics.append(metric_name)

            values.append(value)

        if not metrics:
            return

        plt.figure(figsize=(10, 5))

        plt.bar(metrics, values)

        plt.title("Overall Metrics")

        plt.ylabel("Score")

        plt.xticks(rotation=25)

        plt.tight_layout()

        plt.savefig(
            output_dir / "overall_metrics.png",
            dpi=300,
        )

        plt.close()

    @staticmethod
    def generate_category_scores(
        report: dict,
        output_dir: Path,
    ):

        categories = report.get("categories", {})

        if not categories:
            return

        category_names = []

        scores = []

        for category, metrics in categories.items():

            total = []

            for metric_data in metrics.values():

                value = ChartGenerator._extract_metric(
                    metric_data
                )

                if value is not None:

                    total.append(value)

            if not total:
                continue

            category_names.append(category)

            scores.append(sum(total) / len(total))

        plt.figure(figsize=(10, 5))

        plt.bar(category_names, scores)

        plt.title("Category Performance")

        plt.ylabel("Average Score")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            output_dir / "category_scores.png",
            dpi=300,
        )

        plt.close()

    @staticmethod
    def generate_latency(
        report: dict,
        output_dir: Path,
    ):

        latency = report.get(
            "overall",
            {},
        ).get(
            "latency",
            {},
        )

        if not latency:
            return

        labels = [

            "Mean",

            "Median",

            "Min",

            "Max",

        ]

        values = [

            latency.get("mean", 0),

            latency.get("median", 0),

            latency.get("min", 0),

            latency.get("max", 0),

        ]

        plt.figure(figsize=(8, 5))

        plt.bar(labels, values)

        plt.title("Inference Latency")

        plt.ylabel("Seconds")

        plt.tight_layout()

        plt.savefig(

            output_dir / "latency.png",

            dpi=300,

        )

        plt.close()

    @classmethod
    def generate_all(
        cls,
        report: dict,
        output_dir: str | Path,
    ):

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        cls.generate_overall_metrics(
            report,
            output_dir,
        )

        cls.generate_category_scores(
            report,
            output_dir,
        )

        cls.generate_latency(
            report,
            output_dir,
        )

        print("=" * 70)
        print("Charts generated successfully.")
        print("=" * 70)