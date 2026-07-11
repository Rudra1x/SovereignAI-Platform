"""
Inference backends.
"""

from evaluation.backends.base import BaseBackend
from evaluation.backends.ollama_backend import OllamaBackend

__all__ = [
    "BaseBackend",
    "OllamaBackend",
]