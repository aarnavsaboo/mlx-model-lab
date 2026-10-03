from argparse import ArgumentParser
from pathlib import Path
import json

from .executor import execute, write_jsonl
from .io import read_jobs, read_rows
from .matrix import expand
from .report import summarize


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("config")

    execute_cmd = sub.add_parser("execute")
    execute_cmd.add_argument("plan")
    execute_cmd.add_argument("--output", required=True)
    execute_cmd.add_argument("--workers", type=int, default=1)

    report = sub.add_parser("report")
    report.add_argument("path")

    args = parser.parse_args()

    if args.cmd == "plan":
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        for job in expand(config):
            print(json.dumps(job.to_dict(), sort_keys=True))
    elif args.cmd == "execute":
        rows = execute(read_jobs(args.plan), workers=args.workers)
        write_jsonl(args.output, rows)
        print(json.dumps({"completed": len(rows), "ok": sum(bool(x.get("ok")) for x in rows)}))
    else:
        print(json.dumps(summarize(read_rows(args.path)), indent=2))


if __name__ == "__main__":
    main()
