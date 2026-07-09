from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from sovereign.data.dataset.dataset import Dataset


class BaseExporter(ABC):

    @abstractmethod
    def export(
        self,
        dataset: Dataset,
        output_path: str | Path,
    ) -> None:
        raise NotImplementedError