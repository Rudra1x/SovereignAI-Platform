import re

from sovereign.data.core.transformation_context import (
    TransformationContext,
)

from .base import BaseTransformer


class Cleaner(BaseTransformer):

    def transform(
        self,
        context: TransformationContext,
    ) -> TransformationContext:

        text = context.parsed_content.text

        text = text.replace("\x00", "")

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        context.parsed_content.text = text.strip()

        context.add_step("Cleaner")

        return context