import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from examples.demonstration.planner import plan
from examples.demonstration.__main__ import run

ROOT = Path(__file__).resolve().parents[1]
class DemonstrationTests(unittest.TestCase):
    def test_detects_bug_and_corrected_run_passes(self):
        cases=json.loads((ROOT/"examples/demonstration/cases.json").read_text())
        runs=run(cases)
        self.assertEqual(runs["before"]["report"]["failed"],1)
        self.assertEqual(runs["after"]["report"]["failed"],0)
    def test_planner_handles_unseen_recipient_and_content(self):
        result=plan("Draft an email to new@example.org saying Hello there!")
        self.assertEqual(result["arguments"],{"to":"new@example.org","body":"Hello there!"})
    def test_unknown_input_clarifies(self):
        self.assertEqual(plan("Delete everything")["decision"],"clarify")
    def test_send_requires_confirmation_by_default(self):
        self.assertEqual(plan("Send an email to new@example.org saying Hello")["decision"],"confirm")
    def test_cli_creates_recheckable_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            command=subprocess.run([sys.executable,"-m","examples.demonstration","--output-dir",tmp],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(command.returncode,0,command.stderr)
            self.assertEqual(len(list(Path(tmp).glob("*.json"))),4)
            for label,expected in (("before",1),("after",0)):
                check=subprocess.run([sys.executable,"-m","assistantcheck","examples/demonstration/cases.json",str(Path(tmp)/f"{label}_predictions.json")],cwd=ROOT,capture_output=True,text=True)
                self.assertEqual(check.returncode,expected,check.stderr)
