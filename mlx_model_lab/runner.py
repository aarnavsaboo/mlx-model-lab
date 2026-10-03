from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
import subprocess
import sys


@dataclass
class Run:
    model: str
    prompt_chars: int
    max_tokens: int
    elapsed_seconds: float
    returncode: int
    stdout: str
    stderr: str
    command: list[str]

    def to_dict(self):
        return asdict(self)


def command(model: str, prompt: str, max_tokens: int, temperature: float) -> list[str]:
    return [
        sys.executable, "-m", "mlx_lm.generate",
        "--model", model,
        "--prompt", prompt,
        "--max-tokens", str(max_tokens),
        "--temp", str(temperature),
    ]


def run(model: str, prompt: str, max_tokens: int = 128, temperature: float = 0.0) -> Run:
    cmd = command(model, prompt, max_tokens, temperature)
    started = perf_counter()
    proc = subprocess.run(cmd, text=True, capture_output=True)
    elapsed = perf_counter() - started
    return Run(
        model=model,
        prompt_chars=len(prompt),
        max_tokens=max_tokens,
        elapsed_seconds=elapsed,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        command=cmd,
    )


def read_prompt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")
