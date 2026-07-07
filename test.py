from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from sovereign.data.loaders import LocalLoader

loader = LocalLoader()

resource = loader.load("README.md")

print(resource.filename)
print(resource.mime_type)
print(resource.extension)
print(resource.size_bytes)