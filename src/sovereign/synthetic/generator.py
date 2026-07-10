"""
Synthetic data generation pipeline.
"""

from __future__ import annotations

import time

from sovereign.synthetic.prompt_builder import PromptBuilder
from sovereign.synthetic.ollama_client import OllamaClient
from sovereign.synthetic.json_parser import JSONParser
from sovereign.synthetic.validator import SyntheticValidator
from sovereign.synthetic.dataset_expander import DatasetExpander


class SyntheticGenerator:

    def __init__(self):

        self.prompt_builder = PromptBuilder()

        self.client = OllamaClient()

        self.parser = JSONParser()

        self.validator = SyntheticValidator()

        self.expander = DatasetExpander()

    def generate(
        self,
        chunk,
    ) -> list[dict]:

        prompt = self.prompt_builder.build(chunk)

        last_error = None

        for attempt in range(2):

            try:

                response = self.client.generate(
                    prompt
                )

                structured = self.parser.parse(
                    response
                )

                if not self.validator.validate(
                    structured
                ):

                    raise RuntimeError(
                        "Generated JSON failed validation."
                    )

                return self.expander.expand(
                    chunk,
                    structured,
                )

            except Exception as exc:

                last_error = exc

                if attempt == 0:

                    time.sleep(1)

                    continue

                raise last_error