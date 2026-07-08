from sovereign.data.processors.base import (
    BaseProcessor,
)


class DeduplicationProcessor(
    BaseProcessor
):

    def __init__(
        self,
        strategy,
    ):

        self.strategy = strategy

    def process(
        self,
        context,
    ):

        context.duplicate_score = (
            self.strategy.score(
                context.parsed_content.text
            )
        )

        context.add_step(
            "DeduplicationProcessor"
        )

        return context