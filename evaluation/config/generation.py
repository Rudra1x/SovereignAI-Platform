"""
Generation configuration.

Centralized decoding parameters used by
evaluation and benchmarking.
"""

from __future__ import annotations


# ---------------------------------------------------------
# Production / Evaluation
# ---------------------------------------------------------

DEFAULT_GENERATION_OPTIONS = {

    # Deterministic output
    "temperature": 0.0,

    # Disable randomness
    "top_p": 1.0,

    "top_k": 40,

    # Repeatability
    "seed": 42,

    # Same maximum output length
    "num_predict": 128,

    # Optional penalties
    "repeat_penalty": 1.1,

}


# ---------------------------------------------------------
# Creative generation
# ---------------------------------------------------------

CREATIVE_GENERATION_OPTIONS = {

    "temperature": 0.8,

    "top_p": 0.9,

    "top_k": 40,

    "num_predict": 256,

}