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

pipeline = DataPipeline()

parsed = pipeline.ingest("README.md")

engine = ExtractionEngine(
    KnowledgeExtractor(
        RuleBasedExtractionStrategy()
    )
)

units = engine.run(parsed)

print("=" * 60)

print(f"Knowledge Units : {len(units)}")

print("=" * 60)

for unit in units:

    print(unit.text[:120])

    print("-" * 60)