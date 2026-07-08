from __future__ import annotations

from abc import ABC, abstractmethod

from sovereign.data.core.transformation_context import (
    TransformationContext,
)


class BaseProcessor(ABC):

    @abstractmethod
    def process(
        self,
        context: TransformationContext,
    ) -> TransformationContext:
        raise NotImplementedError