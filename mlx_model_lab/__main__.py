from argparse import ArgumentParser
from pathlib import Path
import json

from .matrix import expand
from .runner import run, read_prompt


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("matrix")
    m.add_argument("config")
    r = sub.add_parser("run")
    r.add_argument("--model", required=True)
    r.add_argument("--prompt")
    r.add_argument("--prompt-file")
    r.add_argument("--max-tokens", type=int, default=128)
    r.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()

    if args.cmd == "matrix":
        cfg = json.loads(Path(args.config).read_text())
        for row in expand(cfg):
            print(json.dumps(row))
        return

    prompt = args.prompt if args.prompt is not None else read_prompt(args.prompt_file)
    print(json.dumps(run(args.model, prompt, args.max_tokens, args.temperature).to_dict(), indent=2))


if __name__ == "__main__":
    main()
