"""
Create a 100-question development benchmark while preserving
the category distribution of the full benchmark.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 42

SOURCE = Path(
    "evaluation/benchmarks/quantum_benchmark_v1.json"
)

TARGET = Path(
    "evaluation/benchmarks/quantum_benchmark_dev.json"
)

TARGET_SIZE = 100


def main():

    random.seed(SEED)

    with open(SOURCE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    by_category = defaultdict(list)

    for question in questions:
        by_category[question["category"]].append(question)

    total = len(questions)

    sampled = []

    for category, items in sorted(by_category.items()):

        proportion = len(items) / total

        n = max(
            1,
            round(proportion * TARGET_SIZE),
        )

        sampled.extend(
            random.sample(
                items,
                min(n, len(items)),
            )
        )

    # Correct any rounding differences
    if len(sampled) > TARGET_SIZE:

        sampled = random.sample(
            sampled,
            TARGET_SIZE,
        )

    elif len(sampled) < TARGET_SIZE:

        remaining = [
            q for q in questions
            if q not in sampled
        ]

        sampled.extend(
            random.sample(
                remaining,
                TARGET_SIZE - len(sampled),
            )
        )

    sampled.sort(
        key=lambda x: x["id"]
    )

    with open(TARGET, "w", encoding="utf-8") as f:
        json.dump(
            sampled,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 60)
    print(f"Original : {len(questions)}")
    print(f"Sampled  : {len(sampled)}")
    print("=" * 60)

    print("\nCategory Distribution\n")

    for category, items in sorted(by_category.items()):

        original = len(items)

        new = sum(
            1
            for q in sampled
            if q["category"] == category
        )

        print(
            f"{category:<25}"
            f"{original:>4} -> {new:>3}"
        )


if __name__ == "__main__":
    main()