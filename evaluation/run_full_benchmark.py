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
    "evaluation/benchmarks/quantum_benchmark_dev.json"
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

    metrics = sorted(
        set(base_report["overall"].keys())
        &
        set(adapter_report["overall"].keys())
    )

    for metric in metrics:

        base_metric = base_report["overall"][metric]

        adapter_metric = adapter_report["overall"][metric]


        def metric_value(value):

            if not isinstance(value, dict):
                return value
            
            if "mean" in value:
                return value["mean"]
            if "f1" in value:
                return value["f1"]
            if "score" in value:
                return value["score"]
            return None
        
        base = metric_value(base_metric)
        adapter = metric_value(adapter_metric)

        if base is None or adapter is None:
            continue
        if adapter > base:
            winner = "QuantumQwen"
            
        if adapter_metric > base_metric:

            winner = "QuantumQwen"
        elif base > adapter:
            winner = "Base"
        else:
            winner = "Tie"
        
        comparison["Winner"][metric] = {
            "winner": winner,

            "base": base,

            "adapter": adapter,
            "improvement percent": 
              round(
                  ((adapter - base) / abs(base)) * 100,
                  2,

              )
              if base != 0 else None,
        }

    save_json(

        comparison,

        RESULTS / "comparison.json",

    )

    return comparison


def main():

    comparator = ModelComparator(

        base_model="qwen2.5:3b-instruct",

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
        
        prediction_file = PREDICTIONS / "base_predictions.json",
        output_dir = RESULTS / "base",
        model_name = "Qwen 2.5B-instruct",
        benchmark_name = "Quantum Benchmark Dev (100)",

    )

    print("\nGenerating QuantumQwen Report...")

    adapter_report = generator.generate(
        prediction_file=PREDICTIONS / "adapter_predictions.json",

        output_dir=RESULTS / "adapter",

        model_name="QuantumQwen v1",

        benchmark_name="Quantum Benchmark Dev (100)",
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