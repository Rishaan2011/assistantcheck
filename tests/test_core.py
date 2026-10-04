import copy
import json
import unittest
from pathlib import Path
from assistantcheck import evaluate
ROOT = Path(__file__).resolve().parents[1]
class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT/"examples/cases.json").read_text())
        self.pred = json.loads((ROOT/"examples/passing.json").read_text())
    def test_complete_run(self):
        self.assertEqual(evaluate(self.cases, self.pred)["score"], 1)
    def test_unconfirmed_send_fails(self):
        bad=json.loads((ROOT/"examples/unsafe.json").read_text())
        report=evaluate(self.cases,bad)
        self.assertEqual(report["failed"],1)
        self.assertFalse(report["results"][1]["passed"])
    def test_missing_case_counts_as_failure(self):
        self.assertEqual(evaluate(self.cases,self.pred[:-1])["failed"],1)
    def test_extra_recipient_fails(self):
        self.pred[0]["arguments"]["cc"]="stranger@example.com"
        self.assertEqual(evaluate(self.cases,self.pred)["failed"],1)
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError): evaluate(self.cases,self.pred+[self.pred[0]])
    def test_unknown_id_rejected(self):
        extra=copy.deepcopy(self.pred[0]);extra["id"]="unexpected"
        with self.assertRaises(ValueError): evaluate(self.cases,self.pred+[extra])
    def test_invalid_decision_rejected(self):
        self.pred[0]["decision"]="maybe"
        with self.assertRaises(ValueError): evaluate(self.cases,self.pred)
    def test_malformed_expected_rejected(self):
        self.cases[0]["expected"]=None
        with self.assertRaises(ValueError): evaluate(self.cases,self.pred)
    def test_empty_suite_rejected(self):
        with self.assertRaises(ValueError): evaluate([],self.pred)
