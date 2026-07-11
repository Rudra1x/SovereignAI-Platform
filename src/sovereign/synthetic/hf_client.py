"""
HF Client
"""

from __future__ import annotations

import torch

from sovereign.synthetic.model_manager import get_model


class HFClient:

    def __init__(self):

        self.model, self.tokenizer = get_model()

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
    ) -> str:

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        generated = outputs[0][inputs.input_ids.shape[1]:]

        return self.tokenizer.decode(
            generated,
            skip_special_tokens=True,
        )
