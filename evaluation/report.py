"""
Generate evaluation reports.
"""

import json


class ReportGenerator:

    def create(
        self,
        metrics,
        output_path,
    ):

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                metrics,
                f,
                indent=4,
            )