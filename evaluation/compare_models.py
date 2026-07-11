"""
Compare multiple models.
"""

from __future__ import annotations

from evaluation.loader import ModelLoader
from evaluation.inference import InferenceEngine
from evaluation.benchmark_runner import BenchmarkRunner


class ModelComparator:

    def __init__(
        self,
        base_model,
    ):

        self.loader = ModelLoader(
            base_model,
        )

    def evaluate_base(
        self,
        benchmark,
        output,
        limit=None,
    ):

        model, tokenizer = self.loader.load_base()

        engine = InferenceEngine(
            model,
            tokenizer,
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
        adapter_path,
        benchmark,
        output,
    ):

        model, tokenizer = self.loader.load_adapter(
            adapter_path,
        )

        engine = InferenceEngine(
            model,
            tokenizer,
        )

        BenchmarkRunner(
            engine,
        ).run(
            benchmark,
            output,
        )

    def evaluate_merged(
        self,
        merged_path,
        benchmark,
        output,
    ):

        model, tokenizer = self.loader.load_merged(
            merged_path,
        )

        engine = InferenceEngine(
            model,
            tokenizer,
        )

        BenchmarkRunner(
            engine,
        ).run(
            benchmark,
            output,
        )