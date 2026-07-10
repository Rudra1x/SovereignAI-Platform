"""
Synthetic data validator.
"""

from __future__ import annotations


class SyntheticValidator:

    REQUIRED_FIELDS = (
        "summary",
        "qa",
        "mcqs",
    )

    OPTIONAL_LIST_FIELDS = (
        "coding_tasks",
        "best_practices",
        "common_mistakes",
    )

    OPTIONAL_STRING_FIELDS = (
        "explanation",
    )

    def validate(
        self,
        data: dict,
    ) -> bool:

        if not isinstance(data, dict):
            return False

        # --------------------------------------------------
        # Required fields
        # --------------------------------------------------

        for field in self.REQUIRED_FIELDS:

            if field not in data:
                return False

        # --------------------------------------------------
        # Required types
        # --------------------------------------------------

        if not isinstance(data["summary"], str):
            return False

        if not isinstance(data["qa"], list):
            return False

        if not isinstance(data["mcqs"], list):
            return False

        # --------------------------------------------------
        # Optional string fields
        # --------------------------------------------------

        for field in self.OPTIONAL_STRING_FIELDS:

            if field in data and not isinstance(data[field], str):
                return False

        # --------------------------------------------------
        # Optional list fields
        # --------------------------------------------------

        for field in self.OPTIONAL_LIST_FIELDS:

            if field in data and not isinstance(data[field], list):
                return False

        return True