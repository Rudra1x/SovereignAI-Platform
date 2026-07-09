"""
JSONL dataset writer.
"""

from __future__ import annotations

import json
from pathlib import Path


class DatasetWriter:

    def __init__(
        self,
        output_path: Path,
        mode: str = "w",
    ):

        self.output_path = Path(output_path)

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.file = open(
            self.output_path,
            mode,
            encoding="utf-8",
        )

    def write(
        self,
        record: dict,
    ):

        self.file.write(
            json.dumps(
                record,
                ensure_ascii=False,
            )
        )

        self.file.write("\n")

    def close(self):

        self.file.close()