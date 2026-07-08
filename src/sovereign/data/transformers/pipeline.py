from sovereign.data.core.transformation_context import (
    TransformationContext,
)


class TransformationPipeline:

    def __init__(self):

        self.transformers = []

    def add(self, transformer):

        self.transformers.append(transformer)

        return self

    def run(
        self,
        context: TransformationContext,
    ):

        for transformer in self.transformers:

            context = transformer.transform(
                context
            )

        return context