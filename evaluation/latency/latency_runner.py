"""
Professional Latency Benchmark

Compares Base Model and QuantumQwen
using Ollama native timing metrics.
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from evaluation.latency.prompt_template import build_prompt
from evaluation.backends.ollama_backend import OllamaBackend
from evaluation.latency.warmup import ModelWarmup
from evaluation.utils import load_json, save_json


NS_TO_SEC = 1_000_000_000


class LatencyRunner:

    def __init__(
        self,
        base_model: str,
        adapter_model: str,
    ):

        self.base = OllamaBackend(base_model)
        self.adapter = OllamaBackend(adapter_model)

    def _run_model(
        self,
        backend,
        question,
    ):

        wall_start = time.perf_counter()

        result = backend.generate_with_metrics(
            question
        )

        wall_latency = (
            time.perf_counter()
            - wall_start
        )

        metrics = result["metrics"]

        eval_duration = (
            metrics["eval_duration"] / NS_TO_SEC
        )

        generated_tokens = (
            metrics["eval_count"]
        )

        if eval_duration > 0:

            tps = (

                generated_tokens

                / eval_duration

            )

        else:

            tps = 0

        return {

            "response": result["response"],

            "wall_latency": round(
                wall_latency,
                3,
            ),

            "total_duration": round(
                metrics["total_duration"]
                / NS_TO_SEC,
                3,
            ),

            "load_duration": round(
                metrics["load_duration"]
                / NS_TO_SEC,
                3,
            ),

            "prompt_eval_duration": round(
                metrics["prompt_eval_duration"]
                / NS_TO_SEC,
                3,
            ),

            "generation_duration": round(
                eval_duration,
                3,
            ),

            "prompt_tokens":
                metrics["prompt_eval_count"],

            "generated_tokens":
                generated_tokens,

            "tokens_per_second":
                round(tps, 2),

            "response_characters":
                len(result["response"]),

            "timestamp":
                datetime.now().isoformat(),
        }

    def benchmark(
        self,
        benchmark_path,
        output_path,
        limit=5,
    ):

        benchmark = load_json(
            benchmark_path
        )[:limit]

        print("=" * 80)
        print("WARMING MODELS")
        print("=" * 80)

        ModelWarmup(
            self.base.model
        ).warmup()

        ModelWarmup(
            self.adapter.model
        ).warmup()

        print("=" * 80)
        print("STARTING LATENCY BENCHMARK")
        print("=" * 80)

        comparison = []

        for idx, sample in enumerate(
            benchmark,
            start=1,
        ):

            print(f"\nQuestion {idx}")

            print("-" * 80)

            print(sample["question"])

            print()

            prompt = build_prompt(
                sample["question"]
            )

            base = self._run_model(
                self.base,
                prompt,
            )

            adapter = self._run_model(
                self.adapter,
                prompt,
            )

            comparison.append(

                {

                    "question_id":
                        sample["id"],

                    "question":
                        sample["question"],

                    "base":
                        base,

                    "quantum":
                        adapter,

                }

            )

            print(
                f"Base     : {base['wall_latency']} sec"
            )

            print(
                f"Quantum  : {adapter['wall_latency']} sec"
            )

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        save_json(
            comparison,
            output_path,
        )

        print()

        print("=" * 80)
        print("LATENCY BENCHMARK COMPLETE")
        print("=" * 80)

        return comparison