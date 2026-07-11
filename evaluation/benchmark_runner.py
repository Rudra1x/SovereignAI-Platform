"""
Runs benchmark evaluation.
"""

from __future__ import annotations

import time

from evaluation.utils import (
    load_json,
    save_json,
)


class BenchmarkRunner:

    def __init__(
        self,
        inference_engine,
    ):

        self.engine = inference_engine

    def run(
        self,
        benchmark_path,
        output_path,
    ):

        benchmark = load_json(
            benchmark_path
        )

        predictions = []

        total = len(
            benchmark
        )

        print(f"\nRunning {total} questions...\n")

        for index, item in enumerate(
            benchmark,
            start=1,
        ):

            start = time.perf_counter()

            answer = self.engine.generate(
                item["question"]
            )

            latency = (
                time.perf_counter()
                - start
            )

            predictions.append(
                {
                    "id": item["id"],
                    "category": item["category"],
                    "difficulty": item["difficulty"],
                    "task": item["task"],
                    "question": item["question"],
                    "reference_answer": item["reference_answer"],
                    "model_answer": answer,
                    "keywords": item["keywords"],
                    "latency": latency,
                }
            )

            print(
                f"[{index}/{total}] "
                f"{latency:.2f}s"
            )

        save_json(
            predictions,
            output_path,
        )

        print("\nFinished.")