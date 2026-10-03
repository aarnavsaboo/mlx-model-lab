from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1
from typing import Any
import json


@dataclass(frozen=True)
class Job:
    id: str
    experiment: str
    model: str
    prompt_file: str
    max_tokens: int
    temperature: float
    repeat: int
    mode: str
    extra_args: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["extra_args"] = list(self.extra_args)
        return row


def make_job(**values: Any) -> Job:
    canonical = {
        "experiment": values["experiment"],
        "model": values["model"],
        "prompt_file": values["prompt_file"],
        "max_tokens": int(values["max_tokens"]),
        "temperature": float(values["temperature"]),
        "repeat": int(values["repeat"]),
        "mode": values["mode"],
        "extra_args": tuple(values.get("extra_args", ())),
    }
    digest = sha1(json.dumps({**canonical, "extra_args": list(canonical["extra_args"])}, sort_keys=True).encode()).hexdigest()[:16]
    return Job(id=digest, **canonical)
