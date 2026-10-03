from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
import os
import subprocess
import sys


@dataclass
class Run:
    model: str
    prompt_file: str
    prompt_chars: int
    max_tokens: int
    temperature: float
    elapsed_seconds: float
    returncode: int
    stdout: str
    stderr: str
    command: list[str]
    environment: dict[str, str]

    def to_dict(self):
        return asdict(self)


def command(model: str, prompt: str, max_tokens: int, temperature: float, extra_args=()) -> list[str]:
    return [
        sys.executable, "-m", "mlx_lm.generate",
        "--model", model,
        "--prompt", prompt,
        "--max-tokens", str(max_tokens),
        "--temp", str(temperature),
        *list(extra_args),
    ]


def run(
    model: str,
    prompt_file: str,
    max_tokens: int = 128,
    temperature: float = 0.0,
    extra_args=(),
) -> Run:
    prompt = Path(prompt_file).read_text(encoding="utf-8")
    cmd = command(model, prompt, max_tokens, temperature, extra_args)
    started = perf_counter()
    proc = subprocess.run(cmd, text=True, capture_output=True)
    elapsed = perf_counter() - started
    env = {
        key: os.environ[key]
        for key in ("MLX_METAL_PREWARM",)
        if key in os.environ
    }
    return Run(
        model=model,
        prompt_file=prompt_file,
        prompt_chars=len(prompt),
        max_tokens=max_tokens,
        temperature=temperature,
        elapsed_seconds=elapsed,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        command=cmd,
        environment=env,
    )
