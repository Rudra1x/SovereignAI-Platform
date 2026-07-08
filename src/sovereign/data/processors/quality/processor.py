from sovereign.data.processors.base import (
    BaseProcessor,
)

from sovereign.data.core.transformation_context import (
    TransformationContext,
)

from .strategy import QualityStrategy


class QualityProcessor(BaseProcessor):

    def __init__(
        self,
        strategy: QualityStrategy,
    ):

        self.strategy = strategy

    def process(
        self,
        context: TransformationContext,
    ):

        context.quality_score = self.strategy.score(
            context.parsed_content.text
        )

        context.add_step(
            "QualityProcessor"
        )

        return context