from itertools import product


def expand(config: dict):
    keys = ["models", "prompt_files", "max_tokens", "temperature"]
    values = [config[k] if isinstance(config[k], list) else [config[k]] for k in keys]
    for model, prompt_file, max_tokens, temperature in product(*values):
        yield {
            "model": model,
            "prompt_file": prompt_file,
            "max_tokens": int(max_tokens),
            "temperature": float(temperature),
        }
