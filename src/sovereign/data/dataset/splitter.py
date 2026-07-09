from __future__ import annotations

import random

from sovereign.data.dataset.dataset import Dataset


class DatasetSplitter:

    def split(
        self,
        dataset: Dataset,
        train_ratio: float = 0.8,
        validation_ratio: float = 0.1,
        seed: int = 42,
    ):

        assert (
            train_ratio + validation_ratio < 1.0
        )

        indices = list(
            range(
                len(dataset.records)
            )
        )

        random.Random(seed).shuffle(
            indices
        )

        train_end = int(
            len(indices) * train_ratio
        )

        validation_end = int(
            len(indices)
            * (
                train_ratio
                + validation_ratio
            )
        )

        train = Dataset(
            name=f"{dataset.name}_train",
            version=dataset.version,
        )

        validation = Dataset(
            name=f"{dataset.name}_validation",
            version=dataset.version,
        )

        test = Dataset(
            name=f"{dataset.name}_test",
            version=dataset.version,
        )

        for index in indices[:train_end]:

            train.add(
                dataset.records[index]
            )

        for index in indices[
            train_end:validation_end
        ]:

            validation.add(
                dataset.records[index]
            )

        for index in indices[
            validation_end:
        ]:

            test.add(
                dataset.records[index]
            )

        return train, validation, test