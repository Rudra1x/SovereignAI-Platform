"""
Quantum evaluation plugin.
"""

from __future__ import annotations

from evaluation.plugins.base import EvaluationPlugin


class QuantumPlugin(EvaluationPlugin):

    name = "quantum"

    QUANTUM_TERMS = {

        "qubit",

        "superposition",

        "entanglement",

        "hadamard",

        "cnot",

        "grover",

        "shor",

        "vqe",

        "qaoa",

        "transpiler",

        "qiskit",

        "noise",

        "sampler",

        "estimator",

    }

    def supports(
        self,
        sample,
    ):

        return True

    def evaluate(
        self,
        sample,
        prediction,
    ):

        answer = prediction["model_answer"].lower()

        hits = sum(

            term in answer

            for term in self.QUANTUM_TERMS

        )

        return {

            "quantum_terms":

                hits,

            "coverage":

                hits

                /

                len(self.QUANTUM_TERMS),

        }