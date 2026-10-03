# Experiment methodology

`mlx-model-lab` treats Apple Silicon inference as a measured system: model loading, prompt processing, generation and memory behavior are recorded separately where possible.

## Run identity

A concrete job is derived from an experiment manifest and includes the model reference, prompt fixture, output budget, warm/cold intent and runtime arguments. Job identifiers are deterministic from the planned inputs so raw observations can be traced back to the manifest.

## Artifact pipeline

```text
manifest
   |
   v
matrix expansion
   |
   v
concrete jobs
   |
   v
MLX-oriented runner
   |
   +--> exact command
   +--> stdout/stderr
   +--> wall time
   +--> memory samples
   |
   v
raw JSONL
   |
   v
grouped reports
```

Reports are derived artifacts. Raw job records should remain unchanged so new summaries can be computed later.

## Measurement discipline

Cold and warm runs are different experiment classes. Prompt-length and output-length sweeps should vary one dimension at a time when the goal is attribution.

Memory numbers are process-level observations rather than a claim about total system memory pressure. Quantized model comparisons should retain the exact model revision and quantization identifier.

## Failure handling

A failed process is still a useful experiment result. Store the exit status, captured output and job identity rather than silently dropping the run from a matrix.

## Reproducibility

For comparisons, record the MLX/MLX-LM version, model revision, generation options and machine configuration together with the raw results. Throughput numbers without that context are not portable benchmark claims.
