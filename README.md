# mlx-model-lab

Experiments for running and comparing local language models with MLX on Apple Silicon.

The lab keeps model configuration, prompt sweeps, process timing and memory samples in machine-readable records so changes in quantization, context length or generation size can be compared without relying on terminal impressions.

## Areas

- MLX-LM command orchestration
- model load vs generation time
- prompt-length and output-length sweeps
- repeated warm runs
- process resident-memory sampling
- quantized model comparisons
- batch matrices that preserve the exact command used

```bash
python -m mlx_model_lab matrix configs/example.json
python -m mlx_model_lab run --model mlx-community/Qwen3-4B-4bit --prompt prompts/short.txt
```

This repository does not bundle model weights or fixed benchmark claims. It is a runner for experiments on the machine where the models actually live.

Maintained by **Aarnav Saboo**.
