from sovereign.data.processors.base import (
    BaseProcessor,
)

from .policy import ValidationPolicy


class ValidationProcessor(
    BaseProcessor
):

    def __init__(
        self,
        policy: ValidationPolicy,
    ):

        self.policy = policy

    def process(
        self,
        context,
    ):

        ok = self.policy.validate(
            context
        )

        if not ok:

            context.warnings.append(
                "Validation failed."
            )

        context.add_step(
            "ValidationProcessor"
        )

        return context