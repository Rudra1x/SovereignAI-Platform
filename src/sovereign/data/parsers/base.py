"""
Abstract parser.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sovereign.data.core.parsed_content import ParsedContent
from sovereign.data.core.resource import RawResource


class BaseParser(ABC):

    @abstractmethod
    def parse(
        self,
        resource: RawResource,
    ) -> ParsedContent:
        raise NotImplementedError