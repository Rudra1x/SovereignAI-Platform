"""
Generate Synthetic Dataset

Reads the canonical corpus, generates synthetic instruction
data using the local LLM, validates the output and writes
instruction tuning samples.

Usage
-----

Generate entire dataset

python scripts/generate_synthetic_dataset.py

Generate first 10 documents

python scripts/generate_synthetic_dataset.py --limit 10

Resume previous generation

python scripts/generate_synthetic_dataset.py --resume
"""

from __future__ import annotations

import argparse
import json
import time

from pathlib import Path
from datetime import datetime

from tqdm import tqdm

from sovereign.synthetic.generator import SyntheticGenerator
from sovereign.synthetic.writer import DatasetWriter


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_CORPUS = (
    ROOT
    / "data"
    / "processed"
    / "canonical_corpus.jsonl"
)

OUTPUT_DIR = (
    ROOT
    / "data"
    / "synthetic"
)

RAW_DATASET = (
    OUTPUT_DIR
    / "instruction_dataset.jsonl"
)

CHECKPOINT_FILE = (
    OUTPUT_DIR
    / "checkpoint.json"
)

LOG_FILE = (
    OUTPUT_DIR
    / "generation.log"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------------------
# Command Line
# ---------------------------------------------------------------------

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum documents to process",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume previous generation",
    )

    return parser.parse_args()


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

def log(message: str):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    line = f"[{timestamp}] {message}"

    print(line)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8",
    ) as f:

        f.write(line)
        f.write("\n")


# ---------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------

class CheckpointManager:

    def __init__(self):

        self.path = CHECKPOINT_FILE

    def exists(self):

        return self.path.exists()

    def load(self):

        if not self.exists():

            return {
                "document_index": 0,
                "generated_samples": 0,
                "failed_documents": 0,
                "elapsed_seconds": 0,
            }

        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def save(
        self,
        index,
        samples,
        failures,
        elapsed,
    ):

        checkpoint = {
            "document_index": index,
            "generated_samples": samples,
            "failed_documents": failures,
            "elapsed_seconds": elapsed,
        }

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                checkpoint,
                f,
                indent=2,
            )


# ---------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------

class Statistics:

    def __init__(self):

        self.start_time = time.time()

        self.documents = 0

        self.samples = 0

        self.failures = 0

        self.retries = 0

    @property
    def elapsed(self):

        return time.time() - self.start_time

    def print_summary(self):

        print()

        print("=" * 70)

        print("Generation Summary")

        print("=" * 70)

        print(f"Documents : {self.documents:,}")

        print(f"Samples   : {self.samples:,}")

        print(f"Failures  : {self.failures:,}")

        print(f"Retries   : {self.retries:,}")

        print(
            f"Elapsed   : {self.elapsed:.2f} sec"
        )

        print("=" * 70)


# ---------------------------------------------------------------------
# Corpus Loader
# ---------------------------------------------------------------------

def load_corpus():

    records = []

    with open(
        CANONICAL_CORPUS,
        "r",
        encoding="utf-8",
    ) as f:

        for line in f:

            records.append(
                json.loads(line)
            )

    return records

# ---------------------------------------------------------------------
# Retry Generation
# ---------------------------------------------------------------------

def generate_with_retry(
    generator: SyntheticGenerator,
    title: str,
    text: str,
    retries: int = 3,
):

    last_exception = None

    for attempt in range(1, retries + 1):

        try:

            samples = generator.generate(
                title=title,
                text=text,
            )

            return samples

        except Exception as exc:

            last_exception = exc

            log(
                f"Retry {attempt}/{retries} : {title}"
            )

            time.sleep(attempt)

    raise last_exception


# ---------------------------------------------------------------------
# Progress Printer
# ---------------------------------------------------------------------

def print_progress(
    stats: Statistics,
    current: int,
    total: int,
):

    elapsed = stats.elapsed

    if current == 0:

        eta = 0

    else:

        eta = (elapsed / current) * (total - current)

    print()

    print("=" * 70)

    print(
        f"Processed : {current:,}/{total:,}"
    )

    print(
        f"Generated : {stats.samples:,}"
    )

    print(
        f"Failures  : {stats.failures}"
    )

    print(
        f"Retries   : {stats.retries}"
    )

    print(
        f"Elapsed   : {elapsed:.2f} sec"
    )

    print(
        f"ETA       : {eta:.2f} sec"
    )

    print("=" * 70)


# ---------------------------------------------------------------------
# Document Processor
# ---------------------------------------------------------------------

def process_document(
    document: dict,
    generator: SyntheticGenerator,
    writer: DatasetWriter,
    stats: Statistics,
):

    samples = generate_with_retry(
        generator,
        title=document["title"],
        text=document["text"],
    )

    for sample in samples:

        sample["document_id"] = document["id"]

        sample["source"] = document["source"]

        sample["document_title"] = document["title"]

        writer.write(sample)

    stats.documents += 1

    stats.samples += len(samples)

    return len(samples)


# ---------------------------------------------------------------------
# Resume Logic
# ---------------------------------------------------------------------

def get_start_index(
    resume: bool,
    checkpoint: CheckpointManager,
):

    if not resume:

        return 0

    state = checkpoint.load()

    log(
        f"Resuming from document {state['document_index']}"
    )

    return state["document_index"]


# ---------------------------------------------------------------------
# Dataset Initializer
# ---------------------------------------------------------------------

def create_writer(
    resume: bool,
):

    if resume:

        writer = DatasetWriter(
            RAW_DATASET,
            mode="a",
        )

    else:

        writer = DatasetWriter(
            RAW_DATASET,
            mode="w",
        )

    return writer