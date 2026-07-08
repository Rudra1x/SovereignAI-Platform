import re

from .strategy import LanguageStrategy


class RuleBasedLanguageStrategy(
    LanguageStrategy
):

    def detect(
        self,
        text: str,
    ) -> str:

        if re.search(r"[\u0900-\u097F]", text):
            return "hi"

        return "en"