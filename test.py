from pathlib import Path

from sovereign.data.pipeline import DataPipeline

from sovereign.data.extraction.engine import (
    ExtractionEngine,
)

from sovereign.data.extraction.extractor import (
    KnowledgeExtractor,
)

from sovereign.data.extraction.generators.pipeline import (
    GeneratorPipeline,
)

from sovereign.data.extraction.generators.qa import (
    QAGenerator,
)

from sovereign.data.extraction.strategies.rule_based import (
    RuleBasedExtractionStrategy,
)

from sovereign.data.dataset import (
    DatasetBuilder,
    DatasetSplitter,
    JSONLExporter,
)

pipeline = DataPipeline()

parsed = pipeline.ingest("README.md")

units = (
    ExtractionEngine(
        KnowledgeExtractor(
            RuleBasedExtractionStrategy()
        )
    )
    .run(parsed)
)

records = (
    GeneratorPipeline()
    .add(QAGenerator())
    .run(units)
)

dataset = (
    DatasetBuilder(
        "Quantum Demo"
    )
    .add_many(records)
    .build()
)

train, validation, test = (
    DatasetSplitter().split(
        dataset
    )
)

exporter = JSONLExporter()

exporter.export(
    train,
    Path("data/processed/train.jsonl"),
)

exporter.export(
    validation,
    Path("data/processed/validation.jsonl"),
)

exporter.export(
    test,
    Path("data/processed/test.jsonl"),
)

print("=" * 60)

print("Datasets exported successfully!")

print(len(train))
print(len(validation))
print(len(test))

print("=" * 60)