"""
Professional PDF report generator.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from evaluation.reports.templates import ReportTemplates


class PDFReportGenerator:

    def generate(
        self,
        report: dict,
        output_dir: str | Path,
    ):

        output_dir = Path(output_dir)

        pdf_file = output_dir / "evaluation_report.pdf"

        styles = getSampleStyleSheet()

        story = []

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        story.append(
            Paragraph(
                ReportTemplates.report_title(),
                styles["Title"],
            )
        )

        story.append(Spacer(1, 0.3 * inch))

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = [

            ["Generated", datetime.now().strftime("%Y-%m-%d %H:%M")],

            ["Framework", "QuantumQwen Evaluation"],

            ["Report Type", "Automatic Benchmark Report"],

        ]

        table = Table(metadata)

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

            ])

        )

        story.append(table)

        story.append(Spacer(1, 0.25 * inch))

        # --------------------------------------------------
        # Executive Summary
        # --------------------------------------------------

        story.append(
            Paragraph(
                "<b>Executive Summary</b>",
                styles["Heading2"],
            )
        )

        story.append(

            Paragraph(

                ReportTemplates.executive_summary(report),

                styles["BodyText"],

            )

        )

        story.append(Spacer(1, 0.2 * inch))

        # --------------------------------------------------
        # Overall Metrics
        # --------------------------------------------------

        story.append(

            Paragraph(

                "<b>Overall Metrics</b>",

                styles["Heading2"],

            )

        )

        data = [["Metric", "Value"]]

        for metric, value in report["overall"].items():

            if isinstance(value, dict):

                if "mean" in value:

                    display = f"{value['mean']:.4f}"

                elif "f1" in value:

                    display = f"{value['f1']:.4f}"

                elif "score" in value:

                    display = f"{value['score']:.4f}"

                else:

                    continue

            else:

                display = str(value)

            data.append([metric, display])

        table = Table(data)

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ])

        )

        story.append(table)

        story.append(Spacer(1, 0.25 * inch))

        # --------------------------------------------------
        # Charts
        # --------------------------------------------------

        chart_names = [

            "overall_metrics.png",

            "category_scores.png",

            "latency.png",

        ]

        for chart in chart_names:

            path = output_dir / chart

            if path.exists():

                story.append(

                    Paragraph(

                        f"<b>{chart}</b>",

                        styles["Heading3"],

                    )

                )

                story.append(

                    Image(

                        str(path),

                        width=6.2 * inch,

                        height=3.8 * inch,

                    )

                )

                story.append(Spacer(1, 0.15 * inch))

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        story.append(

            Paragraph(

                "<b>Recommendations</b>",

                styles["Heading2"],

            )

        )

        for item in ReportTemplates.recommendations(report):

            story.append(

                Paragraph(

                    f"• {item}",

                    styles["BodyText"],

                )

            )

        doc = SimpleDocTemplate(str(pdf_file))

        doc.build(story)

        print(f"PDF written to {pdf_file}")