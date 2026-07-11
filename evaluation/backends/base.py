"""
Base inference backend.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseBackend(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from a prompt.
        """
        raise NotImplementedError