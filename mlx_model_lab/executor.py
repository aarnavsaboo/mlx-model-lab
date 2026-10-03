from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable
import json
import time

from .jobs import Job
from .runner import run


def execute_one(job: Job) -> dict:
    started = time.time()
    result = run(
        job.model,
        job.prompt_file,
        job.max_tokens,
        job.temperature,
        job.extra_args,
    )
    return {
        "job_id": job.id,
        "experiment": job.experiment,
        "repeat": job.repeat,
        "mode": job.mode,
        "started_at": started,
        "ok": result.returncode == 0,
        **result.to_dict(),
    }


def execute(jobs: Iterable[Job], workers: int = 1) -> list[dict]:
    jobs = list(jobs)
    if workers <= 1:
        return [execute_one(job) for job in jobs]
    out = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = [pool.submit(execute_one, job) for job in jobs]
        for future in as_completed(pending):
            out.append(future.result())
    return out


def write_jsonl(path: str, rows: Iterable[dict]):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
