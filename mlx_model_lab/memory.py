from dataclasses import dataclass
from time import monotonic, sleep
import subprocess


@dataclass(frozen=True)
class Sample:
    t: float
    rss_kb: int


def rss_kb(pid: int) -> int:
    out = subprocess.check_output(["ps", "-o", "rss=", "-p", str(pid)], text=True).strip()
    return int(out or 0)


def sample_process(pid: int, interval: float = 0.1, duration: float = 5.0) -> list[Sample]:
    started = monotonic()
    rows = []
    while monotonic() - started <= duration:
        try:
            rows.append(Sample(monotonic() - started, rss_kb(pid)))
        except (subprocess.CalledProcessError, ValueError):
            break
        sleep(interval)
    return rows
