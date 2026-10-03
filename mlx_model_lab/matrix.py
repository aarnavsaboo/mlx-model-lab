from itertools import product
from .jobs import Job, make_job


def _list(value):
    return value if isinstance(value, list) else [value]


def expand(config: dict) -> list[Job]:
    experiment = str(config.get("name", "experiment"))
    models = _list(config["models"])
    prompts = _list(config["prompt_files"])
    max_tokens = _list(config.get("max_tokens", [128]))
    temperatures = _list(config.get("temperature", [0.0]))
    modes = _list(config.get("mode", ["warm"]))
    repeats = range(int(config.get("repeats", 3)))
    extra_args = tuple(config.get("extra_args", []))

    jobs = []
    for model, prompt, limit, temp, mode, repeat in product(
        models, prompts, max_tokens, temperatures, modes, repeats
    ):
        jobs.append(make_job(
            experiment=experiment,
            model=model,
            prompt_file=prompt,
            max_tokens=limit,
            temperature=temp,
            mode=mode,
            repeat=repeat,
            extra_args=extra_args,
        ))
    return jobs
