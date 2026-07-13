"""
Ollama backend.

Supports:

- Standard text generation
- Native performance metrics
- Configurable generation options
"""

from __future__ import annotations

import ollama

from evaluation.config.generation import (
    DEFAULT_GENERATION_OPTIONS,
)


class OllamaBackend:

    def __init__(
        self,
        model: str,
        options: dict | None = None,
    ):
        self.model = model

        self.options = (
            options
            if options is not None
            else DEFAULT_GENERATION_OPTIONS.copy()
        )

    # ---------------------------------------------------------
    # Internal Ollama call
    # ---------------------------------------------------------

    def _chat(
        self,
        prompt: str,
    ):

        return ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            options=self.options,

        )

    # ---------------------------------------------------------
    # Standard generation
    # ---------------------------------------------------------

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self._chat(prompt)

        return response.message.content

    # ---------------------------------------------------------
    # Generation + Native Metrics
    # ---------------------------------------------------------

    def generate_with_metrics(
        self,
        prompt: str,
    ) -> dict:

        response = self._chat(prompt)

        metrics = {

            "total_duration":
                response.total_duration,

            "load_duration":
                response.load_duration,

            "prompt_eval_duration":
                response.prompt_eval_duration,

            "eval_duration":
                response.eval_duration,

            "prompt_eval_count":
                response.prompt_eval_count,

            "eval_count":
                response.eval_count,

            "done_reason":
                response.done_reason,

        }

        return {

            "response": response.message.content,

            "metrics": metrics,

        }