"""
Synthetic data generation pipeline.
"""

from __future__ import annotations

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
        title: str,
        text: str,
    ) -> list[dict]:

        prompt = self.prompt_builder.build(text)

        response = self.client.generate(prompt)

        structured = self.parser.parse(response)

        if not self.validator.validate(structured):

            raise RuntimeError(
                "Generated JSON failed validation."
            )

        return self.expander.expand(
            title,
            structured,
        )