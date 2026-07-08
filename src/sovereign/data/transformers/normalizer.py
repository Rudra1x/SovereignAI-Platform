import unicodedata

from sovereign.data.core.transformation_context import (
    TransformationContext,
)

from .base import BaseTransformer


class Normalizer(BaseTransformer):

    def transform(
        self,
        context: TransformationContext,
    ) -> TransformationContext:

        text = context.parsed_content.text

        text = unicodedata.normalize(
            "NFKC",
            text,
        )

        context.parsed_content.text = text

        context.add_step(
            "Normalizer"
        )

        return context