"""
Model warmup utilities.

Purpose:
    Load models into memory before benchmarking so that
    cold-start latency is excluded from measurements.
"""

from __future__ import annotations

from evaluation.backends.ollama_backend import OllamaBackend


class ModelWarmup:

    def __init__(self, model: str):

        self.backend = OllamaBackend(model)

    def warmup(self):

        print("=" * 70)
        print(f"Warming model: {self.backend.model}")
        print("=" * 70)

        try:

            self.backend.generate(
                "Reply with exactly one word: READY"
            )

            print("✓ Warmup completed.\n")

        except Exception as e:

            print(f"Warmup failed: {e}")

            raise