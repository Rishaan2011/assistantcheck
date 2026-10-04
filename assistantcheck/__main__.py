import argparse
import json
import sys
from pathlib import Path
from .core import evaluate

def main():
    parser = argparse.ArgumentParser(description="Check recorded assistant decisions without executing actions.")
    parser.add_argument("cases", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--report", type=Path, help="Write a machine-readable JSON report")
    args = parser.parse_args()
    try:
        report = evaluate(json.loads(args.cases.read_text()), json.loads(args.predictions.read_text()))
        if args.report:
            args.report.write_text(json.dumps(report, indent=2)+"\n")
    except (OSError, ValueError) as error:
        print(f"Input/report error: {error}", file=sys.stderr)
        return 2
    print(f"{report['passed']}/{report['total']} passed ({report['score']:.0%})")
    for result in report["results"]:
        if not result["passed"]:
            print(f"FAIL {result['id']}: {', '.join(result['failures'])}")
    return 0 if not report["failed"] else 1

if __name__ == "__main__":
    sys.exit(main())
