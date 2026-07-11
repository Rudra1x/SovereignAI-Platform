"""
Utility functions used across evaluation modules.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_json(path: str | Path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: str | Path):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )


def print_header(title: str):

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)