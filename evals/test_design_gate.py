"""Behavioral CLI checks; fixture image bytes do not constitute visual review."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/reference-review/scripts/design_gate.py"


class DesignGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SCRIPT.is_file():
            raise AssertionError(f"Design gate CLI must exist: {SCRIPT}")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "evidence").mkdir()
        (self.root / "src/button.css").write_text("button { background: blue; }\n")
        (self.root / "evidence/screen.png").write_bytes(b"fixture evidence bytes")
        self.catalog = {"schema_version": 1, "version": 1, "rules": [
            {"id": "R1", "status": "active", "checks": ["code", "visual"]}]}
        self.contract = {"schema_version": 1, "catalog_version": 1, "targets": ["src"],
                         "rules": [{"id": "R1", "applicable": True, "scope": "primary CTA",
                                    "reason": "avoid gradients", "checks": ["code", "visual"],
                                    "exceptions": []}]}
        self.write("catalog.json", self.catalog)
        self.write("contract.json", self.contract)
        fingerprint = self.run_cli("fingerprint", expected_exit=0)
        self.report = {"schema_version": 1, "contract_sha256": fingerprint["contract_sha256"],
                       "target_sha256": fingerprint["target_sha256"], "catalog_sha256": fingerprint["catalog_sha256"], "results": [
                           {"id": "R1", "status": "pass", "reason": "checked no gradient",
                            "evidence": [self.evidence("code", "src/button.css"),
                                         self.evidence("visual", "evidence/screen.png")]}]}

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def evidence(self, kind, path):
        return {"kind": kind, "path": path,
                "sha256": hashlib.sha256((self.root / path).read_bytes()).hexdigest()}

    def run_cli(self, command, *extra, expected_exit=None):
        args = [sys.executable, str(SCRIPT), command, "--catalog", str(self.root / "catalog.json"),
                "--contract", str(self.root / "contract.json"), "--root", str(self.root)]
        if command == "check":
            args += ["--report", str(self.root / "report.json")]
        result = subprocess.run(args + list(extra), capture_output=True, text=True, timeout=10)
        if expected_exit is not None:
            self.assertEqual(result.returncode, expected_exit, result.stdout + result.stderr)
        try:
            payload = json.loads(result.stdout)
        except ValueError:
            self.fail(f"CLI did not return JSON: {result.stdout!r}; stderr={result.stderr!r}")
        if command == "check":
            self.assertIn(payload.get("status"), ("PASS", "FAIL", "UNVERIFIED"))
            self.assertEqual(result.returncode, {"PASS": 0, "FAIL": 1, "UNVERIFIED": 2}[payload["status"]])
            self.assertIsInstance(payload.get("errors"), list)
            self.assertTrue(all(isinstance(error, str) for error in payload["errors"]))
        return payload

    def refresh_contract(self):
        self.write("contract.json", self.contract)
        fingerprints = self.run_cli("fingerprint", expected_exit=0)
        for key in ("contract_sha256", "target_sha256", "catalog_sha256"):
            self.report[key] = fingerprints[key]

    def check(self, expected=None, ledger=False):
        self.write("report.json", self.report)
        extra = ["--ledger", str(self.root / "ledger.jsonl")] if ledger else []
        payload = self.run_cli("check", *extra)
        if expected is not None:
            self.assertEqual(payload["status"], expected, payload)
        else:
            self.assertNotEqual(payload["status"], "PASS", payload)
        return payload

    def test_valid_pass(self):
        self.check("PASS")

    def test_failed_result(self):
        self.report["results"][0]["status"] = "fail"
        self.check("FAIL")

    def test_unknown_result(self):
        self.report["results"][0]["status"] = "unknown"
        self.check("UNVERIFIED")

    def test_missing_catalog_rule_in_contract(self):
        self.contract["rules"] = []
        self.refresh_contract()
        self.check()

    def test_catalog_change_invalidates_report(self):
        self.catalog["rules"][0]["title"] = "Changed rule definition"
        self.write("catalog.json", self.catalog)
        self.check()

    def test_missing_result(self):
        self.report["results"] = []
        self.check()

    def test_missing_evidence(self):
        (self.root / "evidence/screen.png").unlink()
        self.check()

    def test_fake_evidence_digest(self):
        self.report["results"][0]["evidence"][1]["sha256"] = "0" * 64
        self.check()

    def test_changed_target_invalidates_report(self):
        (self.root / "src/button.css").write_text("button { background: red; }\n")
        # Updating evidence must not bypass the stale aggregate target fingerprint.
        self.report["results"][0]["evidence"][0] = self.evidence("code", "src/button.css")
        self.check()

    def test_new_target_file_invalidates_report(self):
        (self.root / "src/new.css").write_text("p { color: red; }\n")
        self.check()

    def test_missing_visual_coverage(self):
        self.report["results"][0]["evidence"] = self.report["results"][0]["evidence"][:1]
        self.check()

    def test_declared_exception(self):
        self.contract["rules"][0]["exceptions"] = [
            {"id": "EX1", "reason": "Approved existing treatment"}]
        self.refresh_contract()
        self.report["results"][0].update(status="exception", exception_id="EX1",
                                          reason="Approved existing treatment")
        self.check("PASS")

    def test_undeclared_exception(self):
        self.report["results"][0].update(status="exception", exception_id="EX1",
                                          reason="Unapproved treatment")
        self.check("UNVERIFIED")

    def test_not_applicable_with_reason(self):
        self.contract["rules"][0].update(applicable=False, reason="No primary CTA in scope")
        self.refresh_contract()
        self.report["results"][0].update(status="not-applicable", reason="No primary CTA in scope",
                                          evidence=[])
        self.check("PASS")

    def test_cannot_skip_applicable_rule(self):
        self.report["results"][0].update(status="not-applicable", reason="Skipped", evidence=[])
        self.check()

    def test_changed_contract_invalidates_report(self):
        self.contract["rules"][0]["scope"] = "all buttons"
        self.write("contract.json", self.contract)
        self.check()

    def test_cannot_weaken_catalog_checks(self):
        self.contract["rules"][0]["checks"] = ["code"]
        self.refresh_contract()
        self.report["results"][0]["evidence"] = self.report["results"][0]["evidence"][:1]
        self.check("UNVERIFIED")

    def test_duplicate_result_is_unverified(self):
        self.report["results"].append(dict(self.report["results"][0]))
        self.check("UNVERIFIED")

    def test_incomplete_ledger_is_preserved(self):
        ledger = self.root / "ledger.jsonl"
        original = b'{"interrupted":'
        ledger.write_bytes(original)
        self.check("UNVERIFIED", ledger=True)
        self.assertEqual(ledger.read_bytes(), original)

    def test_default_catalog_requires_all_active_rules(self):
        catalog_path = SCRIPT.parent.parent / "references/failure-catalog.json"
        catalog = json.loads(catalog_path.read_text())
        self.assertEqual(len(catalog["rules"]), 57)
        for prefix, count in [("ORC-F", 16), ("ORC-G", 24), ("ORC-A", 10)]:
            self.assertEqual(sum(r["id"].startswith(prefix) for r in catalog["rules"]), count)
        self.write("report.json", self.report)
        outcome = self.run_cli("check", "--catalog", str(catalog_path), expected_exit=2)
        self.assertEqual(sum("Catalog rule missing" in e for e in outcome["errors"]), 57)

    def test_ledger_deduplication_and_history(self):
        self.check("PASS", ledger=True)
        ledger = self.root / "ledger.jsonl"
        original = ledger.read_bytes()
        self.assertEqual(len(original.splitlines()), 1)
        self.check("PASS", ledger=True)
        self.assertEqual(ledger.read_bytes(), original)
        self.report["results"][0].update(status="fail", reason="A violation was identified")
        self.check("FAIL", ledger=True)
        self.report["results"][0].update(status="pass", reason="Violation fixed and reviewed")
        self.check("PASS", ledger=True)
        final = ledger.read_bytes()
        self.assertTrue(final.startswith(original), "Earlier audit entry must remain unchanged")
        self.assertEqual(len(final.splitlines()), 3)
        for line in final.splitlines():
            self.assertIsInstance(json.loads(line), dict)


if __name__ == "__main__":
    unittest.main()
