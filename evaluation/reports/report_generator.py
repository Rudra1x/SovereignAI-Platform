"""
Evaluation report generator.
"""

from __future__ import annotations

import json
from pathlib import Path

from evaluation.metrics.evaluator import Evaluator


class ReportGenerator:

    def __init__(self):

        self.evaluator = Evaluator()

    def generate(

    self,

    prediction_file,

    output_dir,

):

     output_dir = Path(output_dir)

     output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

     report = self.evaluator.evaluate(

        prediction_file

    )

     metrics_file = output_dir / "metrics.json"

     with open(

        metrics_file,

        "w",

        encoding="utf-8",

     ) as f:

        json.dump(

            report,

            f,

            indent=4,

        )

     from evaluation.reports.markdown import MarkdownReport

     MarkdownReport.write(

        report,

        output_dir / "evaluation_report.md",

    )
     from evaluation.reports.charts import ChartGenerator

     ChartGenerator.generate_all(
      report,
      output_dir,
)

     return report