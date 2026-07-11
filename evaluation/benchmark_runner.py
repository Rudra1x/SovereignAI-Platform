"""
Runs benchmark evaluation.
"""

from __future__ import annotations

import time
from pathlib import Path

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
        limit=None,
    ):

        benchmark = load_json(
            benchmark_path
        )

        if limit is not None:
            benchmark = benchmark[:limit]

        output_path = Path(
            output_path
        )

        # --------------------------------------------------
        # Resume previous run
        # --------------------------------------------------

        if output_path.exists():

            predictions = load_json(
                output_path
            )

            completed = {

                p["id"]

                for p in predictions

            }

            benchmark = [

                item

                for item in benchmark

                if item["id"] not in completed

            ]

            print(
                f"\nResuming benchmark..."
            )

            print(
                f"Completed : {len(completed)}"
            )

        else:

            predictions = []

        total = len(
            benchmark
        )

        print(
            f"\nRemaining Questions : {total}\n"
        )

        if total == 0:

            print(
                "Benchmark already complete."
            )

            return

        overall_start = time.perf_counter()

        for index, item in enumerate(
            benchmark,
            start=1,
        ):

            print("=" * 80)

            print(
                f"[{index}/{total}]"
            )

            print(
                item["question"]
            )

            print("-" * 80)

            start = time.perf_counter()

            answer = self.engine.generate(
                item["question"]
            )

            latency = (
                time.perf_counter()
                - start
            )

            prediction = {

                "id":
                    item["id"],

                "category":
                    item["category"],

                "difficulty":
                    item["difficulty"],

                "task":
                    item["task"],

                "question":
                    item["question"],

                "reference_answer":
                    item["reference_answer"],

                "model_answer":
                    answer,

                "keywords":
                    item["keywords"],

                "latency":
                    latency,

            }

            predictions.append(
                prediction
            )

            # ----------------------------------------------
            # Save after every prediction
            # ----------------------------------------------

            save_json(
                predictions,
                output_path,
            )

            print(
                f"Latency : {latency:.2f} sec"
            )

            print()

        elapsed = (

            time.perf_counter()

            - overall_start

        )

        print("=" * 80)

        print("BENCHMARK COMPLETE")

        print("=" * 80)

        print(
            f"Questions : {len(predictions)}"
        )

        print(
            f"Elapsed   : {elapsed:.2f} sec"
        )

        print(
            f"Average   : {elapsed / len(predictions):.2f} sec/question"
        )