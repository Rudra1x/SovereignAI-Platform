"""
Inference engine.

Uses the configured backend to generate model responses.
"""

from __future__ import annotations

from evaluation.backends.ollama_backend import OllamaBackend


class InferenceEngine:

    def __init__(
        self,
        model: str = "quantumqwen:v1",
    ):
        self.backend = OllamaBackend(
            model=model,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.backend.generate(
            prompt,
        )