from __future__ import annotations

import json
from pathlib import Path

from sovereign.data.dataset.dataset import Dataset

from .base import BaseExporter


class JSONLExporter(BaseExporter):

    def export(
        self,
        dataset: Dataset,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as fp:

            for record in dataset:

                messages = []

                for message in record.conversation.messages:

                    messages.append(
                        {
                            "role": message.role.value,
                            "content": message.content,
                        }
                    )

                sample = {

                    "messages": messages,

                    "metadata": {

                        "source_document":
                            record.metadata.source_document,

                        "language":
                            record.metadata.language,

                        "quality_score":
                            record.metadata.quality_score,

                        "sample_type":
                            record.sample_type.value,

                        "difficulty":
                            record.difficulty.value,
                    },
                }

                fp.write(
                    json.dumps(
                        sample,
                        ensure_ascii=False,
                    )
                )

                fp.write("\n")