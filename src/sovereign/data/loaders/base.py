"""
Abstract loader interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sovereign.data.core.resource import RawResource


class BaseLoader(ABC):

    @abstractmethod
    def load(self, source: str) -> RawResource:
        """
        Load data from a source and return RawResource.
        """
        raise NotImplementedError