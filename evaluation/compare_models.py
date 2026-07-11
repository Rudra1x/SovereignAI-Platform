"""
Compare multiple models using Ollama backends.
"""

from __future__ import annotations

from evaluation.benchmark_runner import BenchmarkRunner
from evaluation.inference import InferenceEngine


class ModelComparator:

    def __init__(
        self,
        base_model: str = "qwen2.5:3b",
        adapter_model: str = "quantumqwen:v1",
    ):

        self.base_model = base_model
        self.adapter_model = adapter_model

    def evaluate_base(
        self,
        benchmark,
        output,
        limit=None,
    ):

        print("\n" + "=" * 80)
        print("BASE MODEL")
        print("=" * 80)

        engine = InferenceEngine(
            model=self.base_model,
        )

        BenchmarkRunner(
            engine,
        ).run(
            benchmark,
            output,
            limit=limit,
        )

    def evaluate_adapter(
        self,
        benchmark,
        output,
        limit=None,
    ):

        print("\n" + "=" * 80)
        print("QUANTUMQWEN V1")
        print("=" * 80)

        engine = InferenceEngine(
            model=self.adapter_model,
        )

        BenchmarkRunner(
            engine,
        ).run(
            benchmark,
            output,
            limit=limit,
        )

    def evaluate_models(
        self,
        benchmark,
        base_output,
        adapter_output,
        limit=None,
    ):

        self.evaluate_base(
            benchmark=benchmark,
            output=base_output,
            limit=limit,
        )

        self.evaluate_adapter(
            benchmark=benchmark,
            output=adapter_output,
            limit=limit,
        )