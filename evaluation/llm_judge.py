"""
LLM Judge
"""

from __future__ import annotations


class LLMJudge:

    def build_prompt(
        self,
        question,
        reference,
        answer,
    ):

        return f"""
You are an expert quantum computing evaluator.

Score the answer from 1-10.

Question

{question}

Reference

{reference}

Answer

{answer}

Evaluate

Technical Correctness

Completeness

Reasoning

Hallucination

Overall Score

Return JSON only.
"""