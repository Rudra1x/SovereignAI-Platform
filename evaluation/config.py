"""
Evaluation configuration.
"""

from pathlib import Path

# ==========================================================
# Models
# ==========================================================

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"

ADAPTER_PATH = Path(
    "outputs/adapter"
)

MERGED_MODEL_PATH = Path(
    "outputs/merged_model"
)

# ==========================================================
# Benchmark
# ==========================================================

BENCHMARK = Path(
    "evaluation/benchmarks/quantum_benchmark_v1.json"
)

# ==========================================================
# Output
# ==========================================================

OUTPUT_DIR = Path(
    "evaluation/predictions"
)

REPORT_DIR = Path(
    "evaluation/reports"
)

# ==========================================================
# Generation
# ==========================================================

MAX_NEW_TOKENS = 512

TEMPERATURE = 0.0

TOP_P = 1.0