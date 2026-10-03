# mlx-model-lab

Local language-model experimentation on Apple Silicon using MLX-oriented workflows.

This repository is a collection of runners and experiment utilities for treating local inference as a repeatable workload rather than a one-off terminal command. It focuses on model loading, prompt processing, generation throughput, memory behaviour, context-length sweeps, quantized variants and batch experiment plans.

The core idea is simple: define an experiment once, expand it into concrete jobs, keep every raw observation, and build reports afterwards.

## Experiment workflow

```text
manifest.json
    |
    v
matrix expansion
    |
    +--> model A / prompt 1 / 64 tokens / cold
    +--> model A / prompt 1 / 64 tokens / warm
    +--> model A / prompt 2 / 256 tokens / warm
    +--> model B / prompt 1 / 64 tokens / cold
    |
    v
job runner
    |
    +--> stdout/stderr capture
    +--> wall clock timing
    +--> process memory samples
    +--> exact command record
    |
    v
raw JSONL
    |
    v
aggregate report
```

## Areas of experimentation

- model load vs steady-state generation time
- prompt-length scaling
- output-length scaling
- repeated warm inference
- 4-bit / 6-bit / 8-bit model variants when available
- process-level resident memory sampling
- batch scheduling across a single workstation
- throughput vs latency at different job concurrency
- small-model vs larger-model task sweeps
- context-window stress tests

## Example

```bash
python -m mlx_model_lab plan configs/workload.example.json > runs/plan.jsonl

python -m mlx_model_lab execute \
  runs/plan.jsonl \
  --output runs/raw.jsonl

python -m mlx_model_lab report runs/raw.jsonl
```

The runner stores the exact command used for each job. That matters because local model behaviour can change with model revision, quantization, generation budget and runtime options.

## Repository layout

- `mlx_model_lab/matrix.py` — Cartesian experiment expansion
- `mlx_model_lab/jobs.py` — workload records and deterministic job IDs
- `mlx_model_lab/runner.py` — MLX-LM process runner
- `mlx_model_lab/memory.py` — process memory sampling
- `mlx_model_lab/executor.py` — sequential/bounded execution
- `mlx_model_lab/report.py` — grouped statistics
- `configs/` — example experiment manifests
- `prompts/` — small reproducible workload fixtures
- `docs/` — experiment design notes
- `tests/` — deterministic tests that do not require model weights

The repository does not commit benchmark leaderboards. Results are meaningful only together with the machine, model build, runtime version and workload that produced them.

Maintained by **Aarnav Saboo**.
