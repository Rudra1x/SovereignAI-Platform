from abc import ABC, abstractmethod

from sovereign.data.core.transformation_context import (
    TransformationContext,
)


class ValidationPolicy(ABC):

    @abstractmethod
    def validate(
        self,
        context: TransformationContext,
    ) -> bool:
        pass