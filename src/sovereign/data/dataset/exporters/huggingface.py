from .base import BaseExporter


class HuggingFaceExporter(BaseExporter):

    def export(
        self,
        dataset,
        output_path,
    ):

        raise NotImplementedError(
            "HF Dataset exporter will be implemented "
            "after introducing datasets library."
        )