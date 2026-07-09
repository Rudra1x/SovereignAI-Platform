from .base import BaseExporter


class ParquetExporter(BaseExporter):

    def export(
        self,
        dataset,
        output_path,
    ):

        raise NotImplementedError(
            "Parquet exporter will be implemented "
            "after introducing PyArrow."
        )