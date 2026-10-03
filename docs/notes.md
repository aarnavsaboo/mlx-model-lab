# Notes

Keep cold model loading separate from steady-state generation. For each model, store the exact MLX model identifier, quantization tag, prompt size, output budget and command line.

Resident memory measured with `ps` is process-level and should not be treated as a perfect accounting of unified memory. It is still useful for relative sweeps on the same machine.

The matrix generator intentionally emits configurations rather than silently executing every combination. Large local-model grids can consume substantial time and disk cache, so the runner leaves scheduling explicit.
