from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sovereign.data.pipeline import DataPipeline

pipeline = DataPipeline()

parsed = pipeline.ingest("README.md")

print("=" * 60)
print("Parser :", parsed.parser_name)
print("Words  :", parsed.word_count)
print("Title  :", parsed.title)
print("=" * 60)
print(parsed.text[:500])