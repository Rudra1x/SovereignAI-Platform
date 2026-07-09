"""
Generate Synthetic Dataset

Reads the canonical corpus, chunks documents into semantic chunks,
generates instruction tuning data using Ollama and writes the
final JSONL dataset.

Usage
-----

Generate full dataset

python scripts/generate_synthetic_dataset.py

Generate first 10 documents

python scripts/generate_synthetic_dataset.py --limit 10

Resume generation

python scripts/generate_synthetic_dataset.py --resume
"""

from __future__ import annotations

import argparse
import json
import time

from pathlib import Path
from datetime import datetime

from tqdm import tqdm

from sovereign.synthetic.chunker import SemanticChunker
from sovereign.synthetic.generator import SyntheticGenerator
from sovereign.synthetic.writer import DatasetWriter


# =====================================================================
# Paths
# =====================================================================

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

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_DATASET = (
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


# =====================================================================
# Command Line
# =====================================================================

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of documents to process",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume previous generation",
    )

    return parser.parse_args()


# =====================================================================
# Logging
# =====================================================================

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


# =====================================================================
# Checkpoint
# =====================================================================

class CheckpointManager:

    def __init__(self):

        self.path = CHECKPOINT_FILE

    def exists(self):

        return self.path.exists()

    def load(self):

        if not self.exists():

            return {

                "document_index": 0,

                "generated_chunks": 0,

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
        *,
        document_index: int,
        generated_chunks: int,
        generated_samples: int,
        failed_documents: int,
        elapsed_seconds: float,
    ):

        checkpoint = {

            "document_index": document_index,

            "generated_chunks": generated_chunks,

            "generated_samples": generated_samples,

            "failed_documents": failed_documents,

            "elapsed_seconds": elapsed_seconds,

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


# =====================================================================
# Statistics
# =====================================================================

class Statistics:

    def __init__(self):

        self.start_time = time.time()

        self.documents = 0

        self.chunks = 0

        self.samples = 0

        self.failures = 0

        self.retries = 0

    @property
    def elapsed(self):

        return time.time() - self.start_time

    def summary(self):

        print()

        print("=" * 70)
        print("Generation Summary")
        print("=" * 70)

        print(f"Documents : {self.documents:,}")
        print(f"Chunks    : {self.chunks:,}")
        print(f"Samples   : {self.samples:,}")
        print(f"Failures  : {self.failures:,}")
        print(f"Retries   : {self.retries:,}")
        print(f"Elapsed   : {self.elapsed:.2f} sec")

        print("=" * 70)


# =====================================================================
# Corpus
# =====================================================================

def load_corpus():

    corpus = []

    with open(
        CANONICAL_CORPUS,
        "r",
        encoding="utf-8",
    ) as f:

        for line in f:

            corpus.append(
                json.loads(line)
            )

    return corpus


# =====================================================================
# Initialization
# =====================================================================

def initialize(resume: bool):

    checkpoint = CheckpointManager()

    writer = DatasetWriter(
        OUTPUT_DATASET,
        mode="a" if resume else "w",
    )

    generator = SyntheticGenerator()

    chunker = SemanticChunker(
        chunk_size=450,
        overlap=75,
        min_chunk_size=120,
    )

    stats = Statistics()

    return (
        checkpoint,
        writer,
        generator,
        chunker,
        stats,
    )

# =====================================================================
# Resume
# =====================================================================

def get_start_index(
    resume: bool,
    checkpoint: CheckpointManager,
) -> int:

    if not resume:

        return 0

    state = checkpoint.load()

    log(
        f"Resuming from document index {state['document_index']:,}"
    )

    return state["document_index"]


# =====================================================================
# Retry
# =====================================================================

def generate_chunk(
    generator: SyntheticGenerator,
    title: str,
    text: str,
    retries: int = 3,
):

    last_exception = None

    for attempt in range(1, retries + 1):

        try:

            return generator.generate(
                title=title,
                text=text,
            )

        except Exception as exc:

            last_exception = exc

            log(
                f"Retry {attempt}/{retries} : {title}"
            )

            time.sleep(attempt)

    raise last_exception


# =====================================================================
# Progress
# =====================================================================

def print_progress(
    stats: Statistics,
    processed: int,
    total: int,
):

    elapsed = stats.elapsed

    if processed == 0:

        eta = 0

    else:

        eta = (
            elapsed / processed
        ) * (
            total - processed
        )

    print()

    print("=" * 70)

    print(
        f"Processed Documents : {processed:,}/{total:,}"
    )

    print(
        f"Generated Chunks    : {stats.chunks:,}"
    )

    print(
        f"Generated Samples   : {stats.samples:,}"
    )

    print(
        f"Failures            : {stats.failures:,}"
    )

    print(
        f"Retries             : {stats.retries:,}"
    )

    print(
        f"Elapsed             : {elapsed:.2f} sec"
    )

    print(
        f"ETA                 : {eta:.2f} sec"
    )

    print("=" * 70)


# =====================================================================
# Process One Document
# =====================================================================

def process_document(
    document: dict,
    chunker: SemanticChunker,
    generator: SyntheticGenerator,
    writer: DatasetWriter,
    stats: Statistics,
):

    chunks = chunker.chunk_document(
        document
    )

    stats.chunks += len(chunks)

    generated_samples = 0

    for chunk in chunks:

        samples = generator.generate(
            chunk
        )

        for sample in samples:

            sample["document_id"] = chunk.document_id

            sample["chunk_id"] = chunk.chunk_id

            sample["title"] = chunk.title

            sample["section"] = chunk.section

            sample["source"] = chunk.source

            sample["word_count"] = chunk.word_count

            writer.write(sample)

        generated_samples += len(samples)

    stats.documents += 1

    stats.samples += generated_samples

    return generated_samples


# =====================================================================
# Generation Loop
# =====================================================================

def run_generation():

    args = parse_args()

    (
        checkpoint,
        writer,
        generator,
        chunker,
        stats,
    ) = initialize(
        resume=args.resume
    )

    corpus = load_corpus()

    if args.limit is not None:

        corpus = corpus[: args.limit]

    total_documents = len(corpus)

    start_index = get_start_index(
        args.resume,
        checkpoint,
    )

    log(
        f"Loaded {total_documents:,} documents."
    )

    progress = tqdm(

        range(start_index, total_documents),

        desc="Generating",

        unit="document",

    )
    for index in progress:

        document = corpus[index]

        progress.set_postfix(
            {
                "docs": stats.documents,
                "chunks": stats.chunks,
                "samples": stats.samples,
                "failed": stats.failures,
            }
        )

        try:

            generated = process_document(
                document=document,
                chunker=chunker,
                generator=generator,
                writer=writer,
                stats=stats,
            )

            checkpoint.save(
                document_index=index + 1,
                generated_chunks=stats.chunks,
                generated_samples=stats.samples,
                failed_documents=stats.failures,
                elapsed_seconds=stats.elapsed,
            )

            log(
                f"[{index + 1}/{total_documents}] "
                f"SUCCESS | "
                f"{generated} samples | "
                f"{document['title']}"
            )

            if (index + 1) % 10 == 0:

                print_progress(
                    stats,
                    index + 1,
                    total_documents,
                )

        except KeyboardInterrupt:

            log(
                "Generation interrupted by user."
            )

            checkpoint.save(
                document_index=index,
                generated_chunks=stats.chunks,
                generated_samples=stats.samples,
                failed_documents=stats.failures,
                elapsed_seconds=stats.elapsed,
            )

            writer.close()

            raise

        except Exception as exc:

            stats.failures += 1

            log(
                f"[{index + 1}/{total_documents}] "
                f"FAILED | "
                f"{document['title']} | "
                f"{type(exc).__name__}: {exc}"
            )

            checkpoint.save(
                document_index=index + 1,
                generated_chunks=stats.chunks,
                generated_samples=stats.samples,
                failed_documents=stats.failures,
                elapsed_seconds=stats.elapsed,
            )

            continue

    writer.close()

    stats.summary()

    # =====================================================================
# Main
# =====================================================================

def main():

    print("=" * 70)
    print("Synthetic Dataset Generation")
    print("=" * 70)
    print()

    start = time.time()

    try:

        run_generation()

    except KeyboardInterrupt:

        print()
        print("=" * 70)
        print("Generation Cancelled")
        print("=" * 70)

    except Exception as exc:

        print()
        print("=" * 70)
        print("Fatal Error")
        print("=" * 70)

        raise

    finally:

        elapsed = time.time() - start

        print()
        print("=" * 70)
        print("Execution Complete")
        print("=" * 70)
        print(f"Execution Time : {elapsed:.2f} sec")
        print("=" * 70)


if __name__ == "__main__":

    main()