"""
Synthetic data validator.
"""

from __future__ import annotations


class SyntheticValidator:

    REQUIRED_FIELDS = (
        "summary",
        "explanation",
        "qa",
        "mcqs",
        "coding_tasks",
        "best_practices",
        "common_mistakes",
    )

    def validate(
        self,
        data: dict,
    ) -> bool:

        if not isinstance(data, dict):
            return False

        for field in self.REQUIRED_FIELDS:

            if field not in data:
                return False

        if not isinstance(data["qa"], list):
            return False

        if not isinstance(data["mcqs"], list):
            return False

        if not isinstance(data["coding_tasks"], list):
            return False

        if not isinstance(data["best_practices"], list):
            return False

        if not isinstance(data["common_mistakes"], list):
            return False

        return True