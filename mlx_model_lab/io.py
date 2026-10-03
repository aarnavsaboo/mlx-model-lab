from pathlib import Path
import json
from .jobs import Job


def read_jobs(path: str) -> list[Job]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            row["extra_args"] = tuple(row.get("extra_args", []))
            rows.append(Job(**row))
    return rows


def read_rows(path: str) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
