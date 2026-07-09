from __future__ import annotations

from sovereign.data.dataset.dataset import Dataset
from sovereign.data.dataset.record import CanonicalRecord


class DatasetBuilder:

    def __init__(
        self,
        name: str,
        version: str = "0.1.0",
    ):

        self.dataset = Dataset(
            name=name,
            version=version,
        )

    def add(
        self,
        record: CanonicalRecord,
    ):

        self.dataset.add(record)

        return self

    def add_many(
        self,
        records: list[CanonicalRecord],
    ):

        self.dataset.extend(records)

        return self

    def build(self):

        return self.dataset