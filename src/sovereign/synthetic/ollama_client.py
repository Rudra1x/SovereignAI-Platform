"""
Simple Ollama client.

All communication with Ollama happens through this class.
"""

from __future__ import annotations

import json
import requests


class OllamaClient:

    def __init__(
        self,
        model: str = "qwen2.5:3b-instruct",
        host: str = "http://localhost:11434",
        timeout: int = 300,
    ) -> None:

        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:

        url = f"{self.host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        print("=" * 70)
        print("OLLAMA REQUEST")
        print("=" * 70)
        print(f"URL      : {url}")
        print(f"MODEL    : {self.model}")
        print(f"HOST     : {self.host}")
        print("=" * 70)

        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout,
        )

        print()
        print("=" * 70)
        print("OLLAMA RESPONSE")
        print("=" * 70)
        print("STATUS :", response.status_code)
        print(response.text)
        print("=" * 70)

        response.raise_for_status()

        data = response.json()

        return data["response"].strip()