"""Run from the repository root: python3 -m examples.demonstration."""
import argparse
import json
from pathlib import Path
from assistantcheck import evaluate
from .planner import plan

def run(cases):
    runs = {}
    for label, confirmation in (("before", False), ("after", True)):
        predictions = [{"id": c["id"], **plan(c["prompt"], require_confirmation=confirmation)}
                       for c in cases]
        runs[label] = {"predictions": predictions, "report": evaluate(cases, predictions)}
    return runs

def main():
    parser = argparse.ArgumentParser(description="Run a synthetic assistant regression demonstration.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/demonstration"))
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    runs = run(cases)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    print("SIMULATED DEMO: rule-based planner; no AI model or actions executed.")
    for label, data in runs.items():
        report = data["report"]
        print(f"{label.upper()}: {report['passed']}/{report['total']} passed")
        for result in report["results"]:
            if not result["passed"]:
                print(f"  FAIL {result['id']}: {', '.join(result['failures'])}")
        for name, value in data.items():
            (args.output_dir/f"{label}_{name}.json").write_text(json.dumps(value, indent=2)+"\n")
    detected = [r["id"] for r in runs["before"]["report"]["results"] if not r["passed"]]
    succeeded = detected == ["send"] and runs["after"]["report"]["failed"] == 0
    print("DEMO VERIFIED" if succeeded else "DEMO FAILED: unexpected results")
    print(f"Generated predictions and reports: {args.output_dir}")
    return 0 if succeeded else 1

if __name__ == "__main__":
    raise SystemExit(main())
