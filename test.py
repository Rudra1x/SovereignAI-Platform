from sovereign.data.pipeline import DataPipeline

from sovereign.data.extraction.engine import (
    ExtractionEngine,
)

from sovereign.data.extraction.extractor import (
    KnowledgeExtractor,
)

from sovereign.data.extraction.strategies.rule_based import (
    RuleBasedExtractionStrategy,
)

from sovereign.data.extraction.generators.pipeline import (
    GeneratorPipeline,
)

from sovereign.data.extraction.generators.qa import (
    QAGenerator,
)

from sovereign.data.dataset import DatasetBuilder

pipeline = DataPipeline()

parsed = pipeline.ingest("README.md")

units = ExtractionEngine(
    KnowledgeExtractor(
        RuleBasedExtractionStrategy()
    )
).run(parsed)

records = (
    GeneratorPipeline()
    .add(QAGenerator())
    .run(units)
)

dataset = (
    DatasetBuilder(
        name="Quantum Demo Dataset"
    )
    .add_many(records)
    .build()
)

print("=" * 60)
print(dataset.name)
print(dataset.version)
print(len(dataset))
print(dataset.task_index)
print(dataset.language_index)
print("=" * 60)