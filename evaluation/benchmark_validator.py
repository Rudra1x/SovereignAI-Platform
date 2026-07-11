"""
Validate benchmark datasets.
"""

from __future__ import annotations


class BenchmarkValidator:

    REQUIRED_FIELDS = {

        "id",

        "category",

        "difficulty",

        "task",

        "question",

        "reference_answer",

        "keywords",

    }

    def validate(
        self,
        benchmark,
    ):

        ids = set()

        for sample in benchmark:

            missing = (
                self.REQUIRED_FIELDS
                - sample.keys()
            )

            if missing:

                raise ValueError(
                    f"Missing fields: {missing}"
                )

            if sample["id"] in ids:

                raise ValueError(
                    f"Duplicate id {sample['id']}"
                )

            ids.add(
                sample["id"]
            )

        return True