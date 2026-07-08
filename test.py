from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

from sovereign.data.pipeline import DataPipeline

from sovereign.data.transformers import (
    Cleaner,
    Normalizer,
    TransformationPipeline,
)

from sovereign.data.core.transformation_context import (
    TransformationContext,
)

pipeline = DataPipeline()

parsed = pipeline.ingest("README.md")

context = TransformationContext(parsed)

transform = (
    TransformationPipeline()
    .add(Cleaner())
    .add(Normalizer())
)

context = transform.run(context)

print("=" * 60)

print(context.processing_history)

print(context.parsed_content.word_count)

print("=" * 60)