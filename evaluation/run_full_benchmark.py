"""
Complete benchmark pipeline.

Workflow

1. Evaluate Base Model
2. Evaluate QuantumQwen
3. Generate Reports
4. Compare Models
"""

from pathlib import Path

from evaluation.compare_models import ModelComparator
from evaluation.reports.report_generator import ReportGenerator
from evaluation.utils import load_json, save_json


BENCHMARK = Path(
    "evaluation/benchmarks/quantum_benchmark_v1.json"
)

PREDICTIONS = Path(
    "evaluation/predictions"
)

RESULTS = Path(
    "evaluation/results"
)

PREDICTIONS.mkdir(
    parents=True,
    exist_ok=True,
)

RESULTS.mkdir(
    parents=True,
    exist_ok=True,
)


def compare_reports(
    base_report: dict,
    adapter_report: dict,
):

    comparison = {

        "base": base_report,

        "adapter": adapter_report,

        "winner": {},

    }

    metrics = [

        "exact_match",

        "keyword_score",

    ]

    for metric in metrics:

        base = base_report["overall"][metric]

        adapter = adapter_report["overall"][metric]

        if adapter > base:

            winner = "QuantumQwen"

        elif base > adapter:

            winner = "Base"

        else:

            winner = "Tie"

        comparison["winner"][metric] = {

            "winner": winner,

            "base": base,

            "adapter": adapter,

        }

    save_json(

        comparison,

        RESULTS / "comparison.json",

    )

    return comparison


def main():

    comparator = ModelComparator(

        base_model="qwen2.5:3b",

        adapter_model="quantumqwen:v1",

    )

    print("=" * 80)
    print("RUNNING BENCHMARK")
    print("=" * 80)

    comparator.evaluate_models(

        benchmark=BENCHMARK,

        base_output=PREDICTIONS / "base_predictions.json",

        adapter_output=PREDICTIONS / "adapter_predictions.json",

    )

    generator = ReportGenerator()

    print("\nGenerating Base Report...")

    base_report = generator.generate(

        PREDICTIONS / "base_predictions.json",

        RESULTS / "base",

    )

    print("\nGenerating QuantumQwen Report...")

    adapter_report = generator.generate(

        PREDICTIONS / "adapter_predictions.json",

        RESULTS / "adapter",

    )

    comparison = compare_reports(

        base_report,

        adapter_report,

    )

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for metric, values in comparison["winner"].items():

        print(

            f"{metric:20} "

            f"{values['winner']}"

        )

    print("\nBenchmark Complete.")


if __name__ == "__main__":

    main()