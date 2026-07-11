"""
Ollama inference backend.
"""

from __future__ import annotations

import ollama

from evaluation.backends.base import BaseBackend


class OllamaBackend(BaseBackend):

    def __init__(
        self,
        model: str = "quantumqwen:v1",
    ):
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            options={
                "temperature": 0,
            },
        )

        return response["message"]["content"]