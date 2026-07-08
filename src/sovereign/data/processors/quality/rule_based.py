from .strategy import QualityStrategy


class RuleBasedQualityStrategy(
    QualityStrategy
):

    def score(
        self,
        text: str,
    ) -> float:

        words = len(text.split())

        if words < 30:
            return 0.2

        if words < 100:
            return 0.6

        return 1.0