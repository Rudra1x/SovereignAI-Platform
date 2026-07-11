"""
Code Evaluation
"""

from __future__ import annotations

import subprocess
import tempfile
import os


class CodeEvaluator:

    def extract_python(
        self,
        text: str,
    ):

        if "```python" in text:

            return (
                text.split("```python")[1]
                .split("```")[0]
                .strip()
            )

        if "```" in text:

            return (
                text.split("```")[1]
                .split("```")[0]
                .strip()
            )

        return text.strip()

    def execute(
        self,
        code: str,
        timeout: int = 15,
    ):

        with tempfile.NamedTemporaryFile(
            suffix=".py",
            delete=False,
            mode="w",
            encoding="utf-8",
        ) as f:

            f.write(code)

            filename = f.name

        try:

            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            return {

                "success": result.returncode == 0,

                "stdout": result.stdout,

                "stderr": result.stderr,

            }

        finally:

            os.remove(filename)