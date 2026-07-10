"""
Benchmark OpenVINO GPU inference using Qwen2.5-3B-Instruct.

Requirements:
    pip install "optimum-intel[openvino]" transformers accelerate

Run:
    python benchmarks/benchmark_openvino.py
"""

from __future__ import annotations

import time

import openvino as ov
from optimum.intel.openvino import OVModelForCausalLM
from transformers import AutoTokenizer


MODEL_ID = "linkanjarad/Qwen2.5-3B-Instruct-openvino"
DEVICE = "GPU"


def main():

    print("=" * 70)
    print("OPENVINO GPU BENCHMARK")
    print("=" * 70)

    core = ov.Core()

    print("\nAvailable devices:")
    for device in core.available_devices:
        print(f"  - {device}")

    if DEVICE not in core.available_devices:
        raise RuntimeError(
            f"{DEVICE} not found. Available: {core.available_devices}"
        )

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
    )

    print("Loading model...")

    start = time.perf_counter()

    model = OVModelForCausalLM.from_pretrained(
        MODEL_ID,
        device=DEVICE,
        trust_remote_code=True,
        compile=True,
    )

    load_time = time.perf_counter() - start

    print(f"\nModel loaded in {load_time:.2f} sec")
    print(f"Running on: {DEVICE}")

    prompt = (
        "Explain Bell State in exactly three concise sentences."
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    print("\nWarm-up inference...")

    model.generate(
        **inputs,
        max_new_tokens=16,
    )

    print("Warm-up complete.")

    print("\nBenchmarking...")

    start = time.perf_counter()

    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=False,
    )

    elapsed = time.perf_counter() - start

    text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)

    print(text)

    print("\nGeneration Time : %.2f sec" % elapsed)

    generated_tokens = outputs.shape[1] - inputs["input_ids"].shape[1]

    print("Generated Tokens :", generated_tokens)

    if generated_tokens > 0:
        print(
            "Tokens/sec : %.2f"
            % (generated_tokens / elapsed)
        )

    print("=" * 70)


if __name__ == "__main__":
    main()