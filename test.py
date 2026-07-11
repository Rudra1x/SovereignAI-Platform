from evaluation.inference import InferenceEngine

engine = InferenceEngine()

print("=" * 80)

print(
    engine.generate(
        "What is a qubit?"
    )
)

print("=" * 80)