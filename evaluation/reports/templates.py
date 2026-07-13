"""
Report templates used by the PDF and Markdown generators.
"""

from __future__ import annotations

from datetime import datetime


class ReportTemplates:

    @staticmethod
    def report_title() -> str:
        return "QuantumQwen Evaluation Report"

    @staticmethod
    def executive_summary(report: dict) -> str:

        overall = report["overall"]

        summary = []

        summary.append(
            f"Evaluation completed on {datetime.now().strftime('%Y-%m-%d %H:%M')}."
        )

        if "bertscore" in overall:

            bert = overall["bertscore"]["f1"]

            summary.append(
                f"The model achieved an average BERTScore F1 of {bert:.3f}."
            )

        if "rouge" in overall:

            rouge = overall["rouge"]["score"]

            summary.append(
                f"Average ROUGE-L score: {rouge:.3f}."
            )

        if "bleu" in overall:

            bleu = overall["bleu"]["score"]

            summary.append(
                f"Corpus BLEU score: {bleu:.2f}."
            )

        latency = overall.get("latency", {})

        if latency:

            summary.append(
                f"Average inference latency: {latency['mean']:.2f} seconds."
            )

        summary.append(
            "This report summarizes the automatic evaluation results "
            "for the QuantumQwen model."
        )

        return " ".join(summary)

    @staticmethod
    def recommendations(report: dict) -> list[str]:

        recommendations = []

        recommendations.append(
            "Review the lowest scoring categories before the next training iteration."
        )

        recommendations.append(
            "Inspect failure cases manually to identify missing concepts."
        )

        recommendations.append(
            "Complement automatic metrics with LLM-as-a-Judge evaluation."
        )

        recommendations.append(
            "Track benchmark results across future QuantumQwen versions."
        )

        return recommendations