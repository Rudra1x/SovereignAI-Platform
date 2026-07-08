from sovereign.data.pipeline import DataPipeline

from sovereign.data.extraction.engine import ExtractionEngine
from sovereign.data.extraction.extractor import KnowledgeExtractor
from sovereign.data.extraction.strategies.rule_based import RuleBasedExtractionStrategy

from sovereign.data.extraction.generators.pipeline import GeneratorPipeline
from sovereign.data.extraction.generators.qa import QAGenerator
from sovereign.data.extraction.generators.summary import SummaryGenerator

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
    .add(SummaryGenerator())
    .run(units)
)

print("=" * 60)
print(f"Knowledge Units : {len(units)}")
print(f"Canonical Records : {len(records)}")
print("=" * 60)

record = records[0]

for message in record.conversation.messages:
    print(message.role.value)
    print(message.content)
    print("-" * 40)