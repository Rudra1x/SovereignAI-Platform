"""
Markdown report writer.
"""

from __future__ import annotations

from pathlib import Path


class MarkdownReport:

    @staticmethod
    def write(

        report,

        output_file,

    ):

        output_file = Path(output_file)

        overall = report["overall"]

        with open(

            output_file,

            "w",

            encoding="utf-8",

        ) as f:

            f.write("# QuantumQwen Evaluation Report\n\n")

            f.write("## Overall\n\n")

            f.write(f"Questions: {overall['questions']}\n\n")

            f.write(

                f"Exact Match: {overall['exact_match']:.3f}\n\n"

            )

            f.write(

                f"Keyword Score: {overall['keyword_score']:.3f}\n\n"

            )

            latency = overall["latency"]

            f.write("## Latency\n\n")

            f.write(

                f"- Mean: {latency['mean']:.2f}s\n"

            )

            f.write(

                f"- Median: {latency['median']:.2f}s\n"

            )

            f.write(

                f"- Min: {latency['min']:.2f}s\n"

            )

            f.write(

                f"- Max: {latency['max']:.2f}s\n\n"

            )

            f.write("## Category Scores\n\n")

            for category, scores in report["categories"].items():

                f.write(f"### {category}\n\n")

                f.write(

                    f"- Questions: {scores['questions']}\n"

                )

                f.write(

                    f"- Exact Match: {scores['exact_match']:.3f}\n"

                )

                f.write(

                    f"- Keyword Score: {scores['keyword_score']:.3f}\n\n"

                )