"""
Hallucination Detection
"""

from __future__ import annotations


class HallucinationDetector:

    def api_hallucination(
        self,
        answer: str,
    ):

        suspicious = [

            "QuantumCircuitBuilder",

            "QuantumRuntimeX",

            "qiskit.ai",

            "IBMQuantumEngine",

            "NoiseReducerV3",
        ]

        found = []

        answer = answer.lower()

        for api in suspicious:

            if api.lower() in answer:

                found.append(api)

        return found