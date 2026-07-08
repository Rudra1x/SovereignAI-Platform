from sovereign.data.core.transformation_context import (
    TransformationContext,
)

from sovereign.data.processors.base import BaseProcessor

from .strategy import LanguageStrategy


class LanguageProcessor(BaseProcessor):

    def __init__(
        self,
        strategy: LanguageStrategy,
    ):

        self.strategy = strategy

    def process(
        self,
        context: TransformationContext,
    ):

        context.language = self.strategy.detect(
            context.parsed_content.text
        )

        context.add_step(
            "LanguageProcessor"
        )

        return context