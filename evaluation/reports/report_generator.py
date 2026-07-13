"""
Evaluation Report Generator

Responsible for:

1. Loading prediction JSON
2. Running the evaluator
3. Saving metrics.json
4. Generating markdown
5. Generating charts
6. Generating PDF
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from evaluation.metrics.evaluator import Evaluator
from evaluation.reports.markdown import MarkdownReport
from evaluation.reports.charts import ChartGenerator
from evaluation.reports.pdf_generator import PDFReportGenerator


class ReportGenerator:

    def __init__(self):

        self.evaluator = Evaluator()

    def generate(
        self,
        prediction_file: str | Path,
        output_dir: str | Path,
        model_name: str = "Unknown",
        benchmark_name: str = "Unknown",
    ) -> dict:

        prediction_file = Path(prediction_file)

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ----------------------------------------------------------
        # Load predictions
        # ----------------------------------------------------------

        with open(
            prediction_file,
            "r",
            encoding="utf-8",
        ) as f:

            predictions = json.load(f)

        # ----------------------------------------------------------
        # Evaluate
        # ----------------------------------------------------------

        with open(
            prediction_file,
            "r",
            encoding="utf-8",
        ) as f:

            predictions = json.load(f)
        report = self.evaluator.evaluate(
            predictions
        )

        # ----------------------------------------------------------
        # Metadata
        # ----------------------------------------------------------

        report["metadata"] = {

            "model": model_name,

            "benchmark": benchmark_name,

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "questions": len(predictions),

        }

        # ----------------------------------------------------------
        # Save JSON
        # ----------------------------------------------------------

        metrics_path = output_dir / "metrics.json"

        with open(
            metrics_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False,
            )

        print(f"Saved metrics -> {metrics_path}")

        # ----------------------------------------------------------
        # Markdown
        # ----------------------------------------------------------

        markdown_path = (
            output_dir
            / "evaluation_report.md"
        )

        MarkdownReport.write(
            report,
            markdown_path,
        )

        print(f"Saved markdown -> {markdown_path}")

        # ----------------------------------------------------------
        # Charts
        # ----------------------------------------------------------

        ChartGenerator.generate_all(
            report,
            output_dir,
        )

        # ----------------------------------------------------------
        # PDF
        # ----------------------------------------------------------

        PDFReportGenerator().generate(
            report,
            output_dir,
        )

        print(
            "\n"
            + "=" * 70
        )

        print("REPORT GENERATION COMPLETE")

        print("=" * 70)

        print(f"Model      : {model_name}")

        print(f"Benchmark  : {benchmark_name}")

        print(f"Questions  : {len(predictions)}")

        print(f"Output     : {output_dir}")

        print("=" * 70)

        return report