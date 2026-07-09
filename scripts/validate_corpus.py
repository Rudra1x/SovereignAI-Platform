"""
Corpus Validation Script

Scans every document in manifest.json and produces

1. validated_manifest.json
2. validation_report.json

This script never stops on failures.
Invalid documents are logged and skipped.

Usage
-----
python scripts/validate_corpus.py
"""

from __future__ import annotations

import hashlib
import json
import traceback
from collections import Counter
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from dataclasses import asdict
from pathlib import Path

from tqdm import tqdm

from sovereign.data.pipeline.ingest import DataPipeline


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    ROOT
    / "data"
    / "artifacts"
    / "manifest.json"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "artifacts"
)

VALIDATED_MANIFEST = (
    OUTPUT_DIR
    / "validated_manifest.json"
)

REPORT_FILE = (
    OUTPUT_DIR
    / "validation_report.json"
)

MAX_WORKERS = 8

MIN_WORDS = 20

MAX_FILE_MB = 25


# ============================================================
# Helpers
# ============================================================

pipeline = DataPipeline()


def sha256(path: Path) -> str:

    digest = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def load_manifest():

    with open(
        MANIFEST_PATH,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


def save_json(
    path: Path,
    obj,
):

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            obj,
            f,
            indent=2,
            ensure_ascii=False,
        )


# ============================================================
# Validation
# ============================================================


def validate_document(
    entry: dict,
):

    path = ROOT / entry["path"]

    result = {
        "source": entry["source"],
        "path": entry["path"],
        "relative_path": entry.get    ("relative_path", ""),
        "extension": entry.get("extension", path.    suffix.lower()),
        "status": "valid",
        "reason": "",
    }

    try:

        if not path.exists():

            result["status"] = "invalid"
            result["reason"] = "missing"

            return result

        size_bytes = path.stat().st_size

        result["size_bytes"] = size_bytes

        result["size_mb"] = round(
            size_bytes / (1024 * 1024),
            3,
        )

        if result["size_mb"] > MAX_FILE_MB:

            result["status"] = "invalid"
            result["reason"] = "file_too_large"

            return result

        result["sha256"] = sha256(path)

        parsed = pipeline.ingest(path)

        if parsed is None:

            result["status"] = "invalid"
            result["reason"] = "parser_returned_none"

            return result

        text = parsed.text.strip()

        if not text:

            result["status"] = "invalid"
            result["reason"] = "empty_document"

            return result

        result["title"] = parsed.title

        #result["language"] = parsed.language
        result["language"] = parsed.metadata.get("language", "unknown")
        result["word_count"] = parsed.word_count

        result["character_count"] = parsed.character_count

        result["line_count"] = len(
            text.splitlines()
        )

        if parsed.word_count < MIN_WORDS:

            result["status"] = "invalid"
            result["reason"] = "too_few_words"

            return result

        return result

    except Exception:

        result["status"] = "invalid"

        result["reason"] = traceback.format_exc()

        return result

# ============================================================
# Main
# ============================================================


def main():

    manifest = load_manifest()

    print("=" * 70)
    print("Corpus Validation")
    print("=" * 70)
    print(f"Documents : {len(manifest)}")
    print()

    results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
    ) as executor:

        futures = [

            executor.submit(
                validate_document,
                document,
            )

            for document in manifest

        ]

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Validating",
        ):

            results.append(
                future.result()
            )

    # -------------------------------------------------------
    # Duplicate Detection
    # -------------------------------------------------------

    hash_counter = Counter()

    for result in results:

        if result["status"] == "valid":

            hash_counter[
                result["sha256"]
            ] += 1

    duplicate_count = 0

    for result in results:

        if result["status"] != "valid":

            continue

        if hash_counter[
            result["sha256"]
        ] > 1:

            duplicate_count += 1

            result["status"] = "invalid"

            result["reason"] = "duplicate_document"

    # -------------------------------------------------------
    # Split
    # -------------------------------------------------------

    valid_documents = [

        result

        for result in results

        if result["status"] == "valid"

    ]

    invalid_documents = [

        result

        for result in results

        if result["status"] != "valid"

    ]

    # -------------------------------------------------------
    # Statistics
    # -------------------------------------------------------

    reason_counter = Counter()

    source_counter = Counter()

    extension_counter = Counter()

    total_words = 0

    total_size = 0

    for document in valid_documents:

        source_counter[
            document["source"]
        ] += 1

        extension_counter[
            document["extension"]
        ] += 1

        total_words += document[
            "word_count"
        ]

        total_size += document[
            "size_bytes"
        ]

    for document in invalid_documents:

        reason_counter[
            document["reason"]
        ] += 1

    report = {

        "total_documents": len(results),

        "valid_documents": len(
            valid_documents
        ),

        "invalid_documents": len(
            invalid_documents
        ),

        "duplicate_documents": duplicate_count,

        "total_words": total_words,

        "total_size_mb": round(
            total_size / (1024 * 1024),
            2,
        ),

        "sources": dict(
            source_counter
        ),

        "extensions": dict(
            extension_counter
        ),

        "invalid_reasons": dict(
            reason_counter
        ),

    }

    # -------------------------------------------------------
    # Save
    # -------------------------------------------------------

    save_json(
        VALIDATED_MANIFEST,
        valid_documents,
    )

    save_json(
        REPORT_FILE,
        report,
    )

    invalid_path = (
        OUTPUT_DIR
        / "invalid_documents.json"
    )

    save_json(
        invalid_path,
        invalid_documents,
    )

    # -------------------------------------------------------
    # Console
    # -------------------------------------------------------

    print()
    print("=" * 70)
    print("Validation Complete")
    print("=" * 70)

    print(
        f"Total      : {len(results)}"
    )

    print(
        f"Valid      : {len(valid_documents)}"
    )

    print(
        f"Invalid    : {len(invalid_documents)}"
    )

    print(
        f"Duplicates : {duplicate_count}"
    )

    print(
        f"Words       : {total_words:,}"
    )

    print(
        f"Corpus Size : {report['total_size_mb']} MB"
    )

    print()
    print(
        f"Validated Manifest : {VALIDATED_MANIFEST}"
    )

    print(
        f"Validation Report  : {REPORT_FILE}"
    )

    print(
        f"Invalid Documents  : {invalid_path}"
    )

# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    import time
    import sys

    start = time.perf_counter()

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("=" * 70)
        print("Validation interrupted by user.")
        print("=" * 70)

        sys.exit(1)

    except Exception:

        print()
        print("=" * 70)
        print("Fatal Error")
        print("=" * 70)

        traceback.print_exc()

        sys.exit(1)

    finally:

        elapsed = time.perf_counter() - start

        print()
        print("=" * 70)
        print(f"Execution Time : {elapsed:.2f} seconds")
        print("=" * 70)