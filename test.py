from evaluation.latency.latency_runner import LatencyRunner

runner = LatencyRunner(
    base_model="qwen2.5:3b-instruct",
    adapter_model="quantumqwen:v1",
)

runner.benchmark(
    benchmark_path="evaluation/benchmarks/quantum_benchmark_dev.json",
    output_path="evaluation/latency/comparison.json",
    limit=5,
)