"""
Synthetic data generation pipeline.
"""

from __future__ import annotations

import time
from pprint import pprint

from sovereign.synthetic.prompt_builder import PromptBuilder
from sovereign.synthetic.hf_client import HFClient
from sovereign.synthetic.json_parser import JSONParser
from sovereign.synthetic.validator import SyntheticValidator
from sovereign.synthetic.dataset_expander import DatasetExpander


class SyntheticGenerator:

    DEBUG = False


    def __init__(self):

        self.prompt_builder = PromptBuilder()

        self.client = HFClient()

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

                if self.DEBUG:
                    print("\n" + "=" * 80)
                    print("RAW RESPONSE")
                    print("=" * 80)
                    print(response)
                    print("=" * 80)

                structured = self.parser.parse(
                    response
                )

                if self.DEBUG:
                    print("\n" + "=" * 80)
                    print("PARSED JSON")
                    print("=" * 80)
                    pprint(structured, width=120)
                    print("=" * 80)

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
