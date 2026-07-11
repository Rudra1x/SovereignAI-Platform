"""
Smoke Test

Runs the first 10 benchmark questions against:

1. Base Qwen
2. QuantumQwen v1

This verifies the complete evaluation pipeline before
running the full benchmark.
"""

from pathlib import Path

from evaluation.compare_models import ModelComparator


BENCHMARK = Path(
    "evaluation/benchmarks/quantum_benchmark_v1.json"
)

OUTPUT_DIR = Path(
    "evaluation/predictions"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def main():

    comparator = ModelComparator(

        base_model="qwen2.5:3b-instruct",

        adapter_model="quantumqwen:v1",

    )

    print("=" * 80)
    print("SMOKE TEST")
    print("=" * 80)

    comparator.evaluate_models(

        benchmark=BENCHMARK,

        base_output=OUTPUT_DIR / "base_smoke.json",

        adapter_output=OUTPUT_DIR / "adapter_smoke.json",

        limit=10,

    )

    print()

    print("=" * 80)
    print("SMOKE TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":

    main()