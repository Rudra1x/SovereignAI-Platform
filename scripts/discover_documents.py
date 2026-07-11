from __future__ import annotations

import json
from pathlib import Path

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/artifacts")
OUTPUT_FILE = OUTPUT_DIR / "manifest.json"

# Extensions we actually want to train on
VALID_EXTENSIONS = {
    ".md",
    ".mdx",
    ".txt",
    ".pdf",
    ".ipynb",
}

# Directories we never want to scan
IGNORE_DIRECTORIES = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    "venv",
    ".venv",
    "env",
    "scripts",
    "test",
    "tests",
    "images",
    "assets",
    "static",
    "extracted-outputs",

    # Generated documentation
    "api",
    "_build",
    "_modules",
    "generated",
    "stubs",
}

manifest = []



def should_skip(path: Path) -> bool:

    parts = [p.lower() for p in path.parts]

    # Ignore directories
    if any(part in IGNORE_DIRECTORIES for part in parts):
        return True

    filename = path.name.lower()

    # Ignore project metadata
    skip_files = (
        "license",
        "copying",
        "authors",
        "code_of_conduct",
        "contributing",
        "security",
        "changelog",
        "release_notes",
        "release-notes",
    )

    if any(name in filename for name in skip_files):
        return True

    # Ignore versioned API documentation
    if "docs" in parts and "api" in parts:
        return True

    return False


def discover():

    for file in RAW_DIR.rglob("*"):

        if not file.is_file():
            continue

        if should_skip(file):
            continue

        if file.suffix.lower() not in VALID_EXTENSIONS:
            continue

        source = file.relative_to(RAW_DIR).parts[0]

        manifest.append(
            {
                "source": source,
                "path": str(file),
                "relative_path": str(file.relative_to(RAW_DIR)),
                "extension": file.suffix.lower(),
                "size_bytes": file.stat().st_size,
            }
        )


def save():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest.sort(
        key=lambda x: (
            x["source"],
            x["relative_path"],
        )
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            manifest,
            fp,
            indent=4,
            ensure_ascii=False,
        )


def print_statistics():

    print("=" * 70)

    print("Document Discovery Complete")

    print("=" * 70)

    print(f"Total Documents : {len(manifest)}")

    print()

    counts = {}

    for item in manifest:
        counts[item["source"]] = counts.get(
            item["source"],
            0,
        ) + 1

    print("Documents Per Source")

    print("-" * 70)

    for source, count in sorted(counts.items()):
        print(f"{source:<20} {count}")

    print()

    print(f"Manifest : {OUTPUT_FILE}")

    print("=" * 70)


def main():

    discover()

    save()

    print_statistics()


if __name__ == "__main__":
    main()