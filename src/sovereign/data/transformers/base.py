from __future__ import annotations

from abc import ABC, abstractmethod

from sovereign.data.core.transformation_context import (
    TransformationContext,
)


class BaseTransformer(ABC):

    @abstractmethod
    def transform(
        self,
        context: TransformationContext,
    ) -> TransformationContext:
        pass