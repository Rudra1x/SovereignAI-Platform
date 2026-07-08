from .policy import ValidationPolicy


class DefaultValidationPolicy(
    ValidationPolicy
):

    def validate(
        self,
        context,
    ):

        return (
            len(
                context.parsed_content.text
            )
            > 100
        )