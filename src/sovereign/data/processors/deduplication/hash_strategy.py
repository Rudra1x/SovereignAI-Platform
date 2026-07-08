import hashlib

from .strategy import (
    DeduplicationStrategy,
)


class HashStrategy(
    DeduplicationStrategy
):

    def score(
        self,
        text,
    ):

        hashlib.sha256(
            text.encode()
        ).hexdigest()

        return 0.0