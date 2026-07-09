"""
Build Canonical Corpus

Reads the validated manifest, parses every validated document,
normalizes the content and produces the canonical corpus used
for dataset generation.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from tqdm import tqdm

from sovereign.data.pipeline.ingest import DataPipeline
from sovereign.data.transformers.canonicalizer import Canonicalizer


ROOT = Path(__file__).resolve().parents[1]

VALIDATED_MANIFEST = (
    ROOT
    / "data"
    / "artifacts"
    / "validated_manifest.json"
)

OUTPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "canonical_corpus.jsonl"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_manifest() -> list[dict]:
    with open(VALIDATED_MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def build_document_id(relative_path: str) -> str:
    return hashlib.sha256(relative_path.encode("utf-8")).hexdigest()


def write_record(record: dict) -> None:
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False))
        f.write("\n")


def main():
    start = time.time()
    
    pipeline = DataPipeline()
    canonicalizer = Canonicalizer()
    manifest = load_manifest()

    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    processed = 0
    total_words = 0
    
    # [Fix 3] Initialize parser statistics
    parser_stats = {}

    print("=" * 70)
    print("Building Canonical Corpus")
    print("=" * 70)
    print(f"Documents : {len(manifest)}")
    print()
    failed = 0
    for entry in tqdm(manifest,
                      desc="Canonicalizing",):
        path = Path(entry["path"])

        try:
            # [Fix 1] Explicitly cast Path to string
            parsed = pipeline.ingest(str(path))
            canonical_text = canonicalizer.clean(parsed.text)

            if not canonical_text:
                continue

            record = {
                # [Fix 2] Ensure globally unique IDs by prepending the source
                "id": build_document_id(f'{entry["source"]}:{entry["relative_path"]}'),
                "source": entry["source"],
                "relative_path": entry["relative_path"],
                "title": parsed.title or path.stem,
                "text": canonical_text,
                "language": parsed.metadata.get("language", "unknown"),
                "word_count": len(canonical_text.split()),
                "character_count": len(canonical_text),
                "parser": parsed.metadata.get("parser", "unknown"),
                "headings": parsed.headings,
                "links": parsed.links,
                "metadata": parsed.metadata,
            }

            write_record(record)
            
            # [Fix 3] Track parser usage
            parser_name = parsed.metadata.get("parser", "unknown")
            parser_stats[parser_name] = (
                parser_stats.get(parser_name, 0) + 1
            )
            
            processed += 1
            total_words += record["word_count"]

        except Exception as exc:
            failed += 1
            print()
            print(f"Failed : {path}")
            print(exc)

    print()
    print("=" * 70)
    print("Canonical Corpus Complete")
    print("=" * 70)
    print(f"Documents : {processed}")
    print(f"Words     : {total_words:,}")
    print(f"Output    : {OUTPUT_FILE}")
    print(f"Execution Time : {time.time() - start:.2f} sec")
    
    # [Fix 3] Print Parser Statistics before the final separator
    print()
    print("Parser Usage")
    print("-" * 70)
    for parser, count in sorted(parser_stats.items()):
        print(f"{parser:<20} {count}")
    print("=" * 70)


if __name__ == "__main__":
    main()