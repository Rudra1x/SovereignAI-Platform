from sovereign.data.pipeline import DataPipeline

from sovereign.data.transformers import (
    Cleaner,
    Normalizer,
    TransformationPipeline,
)

from sovereign.data.core.transformation_context import (
    TransformationContext,
)

from sovereign.data.processors.language.processor import (
    LanguageProcessor,
)

from sovereign.data.processors.language.rule_based import (
    RuleBasedLanguageStrategy,
)

from sovereign.data.processors.quality.processor import (
    QualityProcessor,
)

from sovereign.data.processors.quality.rule_based import (
    RuleBasedQualityStrategy,
)

pipeline = DataPipeline()

parsed = pipeline.ingest("README.md")

context = TransformationContext(parsed)

TransformationPipeline()\
.add(Cleaner())\
.add(Normalizer())\
.run(context)

LanguageProcessor(
    RuleBasedLanguageStrategy()
).process(context)

QualityProcessor(
    RuleBasedQualityStrategy()
).process(context)

print(context.language)
print(context.quality_score)
print(context.processing_history)