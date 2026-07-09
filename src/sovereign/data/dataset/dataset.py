from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from sovereign.data.dataset.record import CanonicalRecord


@dataclass(slots=True)
class Dataset:

    name: str

    version: str = "0.1.0"

    records: list[CanonicalRecord] = field(default_factory=list)

    task_index: dict[str, list[int]] = field(
        default_factory=lambda: defaultdict(list)
    )

    language_index: dict[str, list[int]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def add(
        self,
        record: CanonicalRecord,
    ) -> None:

        index = len(self.records)

        self.records.append(record)

        self.task_index[
            record.sample_type.value
        ].append(index)

        self.language_index[
            record.metadata.language
        ].append(index)

    def extend(
        self,
        records: list[CanonicalRecord],
    ) -> None:

        for record in records:
            self.add(record)

    def __len__(self):

        return len(self.records)

    def __iter__(self):

        return iter(self.records)

    def get_by_task(
        self,
        task: str,
    ) -> list[CanonicalRecord]:

        return [
            self.records[i]
            for i in self.task_index.get(task, [])
        ]

    def get_by_language(
        self,
        language: str,
    ) -> list[CanonicalRecord]:

        return [
            self.records[i]
            for i in self.language_index.get(language, [])
        ]