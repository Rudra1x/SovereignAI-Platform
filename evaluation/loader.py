from pathlib import Path

import torch

from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


class ModelLoader:

    def __init__(
        self,
        base_model: str,
    ):
        self.base_model = base_model

    def load_base(self):

        tokenizer = AutoTokenizer.from_pretrained(
            self.base_model,
        )

        model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        model.eval()

        return model, tokenizer

    def load_adapter(
        self,
        adapter_path: str,
    ):

        tokenizer = AutoTokenizer.from_pretrained(
            adapter_path,
        )

        base = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        model = PeftModel.from_pretrained(
            base,
            adapter_path,
        )

        model.eval()

        return model, tokenizer

    def load_merged(
        self,
        merged_path: str,
    ):

        tokenizer = AutoTokenizer.from_pretrained(
            merged_path,
        )

        model = AutoModelForCausalLM.from_pretrained(
            merged_path,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        model.eval()

        return model, tokenizer