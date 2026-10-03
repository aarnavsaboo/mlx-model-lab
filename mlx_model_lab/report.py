from collections import defaultdict
from statistics import median


def summarize(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        if row.get("ok"):
            key = (row["experiment"], row["model"], row["prompt_file"], row["max_tokens"], row["mode"])
            groups[key].append(row)

    out = []
    for key, group in sorted(groups.items()):
        times = sorted(float(x["elapsed_seconds"]) for x in group)
        p90_index = round((len(times) - 1) * .9)
        experiment, model, prompt_file, max_tokens, mode = key
        out.append({
            "experiment": experiment,
            "model": model,
            "prompt_file": prompt_file,
            "max_tokens": max_tokens,
            "mode": mode,
            "runs": len(group),
            "median_seconds": median(times),
            "p90_seconds": times[p90_index],
            "fastest_seconds": min(times),
            "slowest_seconds": max(times),
        })
    return out
