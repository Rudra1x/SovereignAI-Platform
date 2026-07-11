"""
End-to-end evaluation pipeline.
"""

from evaluation.compare_models import ModelComparator

from evaluation.config import *

comparator = ModelComparator(
    BASE_MODEL,
)

print("=" * 80)
print("BASE MODEL")
print("=" * 80)

comparator.evaluate_base(
    BENCHMARK,
    OUTPUT_DIR / "base_predictions.json",
)

print("=" * 80)
print("ADAPTER")
print("=" * 80)

comparator.evaluate_adapter(
    ADAPTER_PATH,
    BENCHMARK,
    OUTPUT_DIR / "adapter_predictions.json",
)

print("=" * 80)
print("MERGED MODEL")
print("=" * 80)

comparator.evaluate_merged(
    MERGED_MODEL_PATH,
    BENCHMARK,
    OUTPUT_DIR / "merged_predictions.json",
)

print("=" * 80)
print("Evaluation Finished")
print("=" * 80)