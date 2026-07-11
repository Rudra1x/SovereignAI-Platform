"""
Shared Model Manager
"""

from __future__ import annotations

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

_MODEL = None
_TOKENIZER = None


def get_model():

    global _MODEL
    global _TOKENIZER

    if _MODEL is None:

        print("=" * 70)
        print("Loading Qwen2.5-3B...")
        print("=" * 70)

        _TOKENIZER = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
        )

        _MODEL = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )

        _MODEL.eval()

        print("Model Loaded.")

    return _MODEL, _TOKENIZER
