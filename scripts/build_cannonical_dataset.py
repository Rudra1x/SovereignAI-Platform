"""
Canonical text transformer.

Converts parsed document text into a normalized representation
that can be consumed by dataset builders and fine-tuning
pipelines.
"""

from __future__ import annotations

import re
import json
import time
import hashlib
from pathlib import Path
from tqdm import tqdm
from sovereign.data.pipeline.ingest import ingest
# --- Placeholders for external constants/functions ---
# Replace these with your actual configurations/imports
VALIDATED_MANIFEST = "manifest.json"
OUTPUT_FILE = Path("output_corpus.jsonl")

def ingest(path: Path):
    """Placeholder for the document ingestion logic."""
    pass
# -----------------------------------------------------

class Canonicalizer:
    """
    Normalize parsed document text.
    
    This class MUST NOT:
    - read files
    - write files
    - know anything about manifests

    Its only responsibility is:
    Raw Text -> Canonical Text
    """

    _MULTIPLE_NEWLINES = re.compile(r"\n{3,}")
    _MULTIPLE_SPACES = re.compile(r"[ \t]+")

    def clean(self, text: str) -> str:
        """
        Convert raw parser output into canonical text.
        """
        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove trailing whitespace
        text = "\n".join(line.rstrip() for line in text.splitlines())

        # Collapse multiple spaces
        text = self._MULTIPLE_SPACES.sub(" ", text)

        # Collapse excessive blank lines
        text = self._MULTIPLE_NEWLINES.sub("\n\n", text)

        return text.strip()


def load_manifest() -> list[dict]:
    with open(VALIDATED_MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def build_document_id(relative_path: str) -> str:
    return hashlib.sha256(
        relative_path.encode("utf-8")
    ).hexdigest()


def write_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False))
        f.write("\n")


def main():
    start = time.time()

    manifest = load_manifest()
    canonicalizer = Canonicalizer()

    total_words = 0
    processed = 0

    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    print("=" * 70)
    print("Building Canonical Corpus")
    print("=" * 70)
    print(f"Documents : {len(manifest)}")
    print()

    for entry in tqdm(manifest):
        path = Path(entry["path"])

        try:
            parsed = ingest(path)
            text = canonicalizer.clean(parsed.text)

            record = {
                "id": build_document_id(entry["relative_path"]),
                "source": entry["source"],
                "relative_path": entry["relative_path"],
                "title": parsed.title or path.stem,
                "text": text,
                "language": entry.get("language", "unknown"),
                "word_count": len(text.split()),
                "character_count": len(text),
                "parser": parsed.parser_name,
                "metadata": parsed.metadata,
            }

            write_jsonl(OUTPUT_FILE, record)

            processed += 1
            total_words += record["word_count"]

        except Exception as exc:
            print(f"Failed : {path}")
            print(exc)

    print()
    print("=" * 70)
    print("Canonical Corpus Complete")
    print("=" * 70)
    print(f"Documents : {processed}")
    print(f"Words     : {total_words:,}")
    print(f"Output    : {OUTPUT_FILE}")
    print(f"Time      : {time.time() - start:.2f} sec")
    print("=" * 70)


if __name__ == "__main__":
    main()