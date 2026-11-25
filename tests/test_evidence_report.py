import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import evidence_report as report
from tools.evidence_model import parse_evidence


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "evidence_report.py"
EXAMPLE = ROOT / "examples" / "synthetic-evidence.json"
GOLDEN = ROOT / "tests" / "fixtures"
LIMIT = 1048576


class TestEvidenceReport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.raw = json.loads(EXAMPLE.read_bytes())

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                              capture_output=True, timeout=10, check=False)

    def put(self, data, name="PRIVATE_MARKER.json"):
        path = self.directory / name
        path.write_bytes(data if isinstance(data, bytes) else json.dumps(data).encode("utf-8"))
        return path

    def assert_error(self, result, code, message):
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (code, b"", message.encode("utf-8")))

    def test_json_report_contract(self):
        result = self.cli("--file", EXAMPLE, "--format", "json")
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        payload = json.loads(result.stdout)
        self.assertEqual(list(payload), ["schema_version", "catalog_version", "source_kind", "summary", "controls"])
        self.assertEqual((payload["schema_version"], payload["catalog_version"], payload["source_kind"]),
                         (1, 1, "synthetic"))
        self.assertEqual(payload["summary"], {
            "catalog_total": 5, "total": 5, "omitted": 0, "met": 2,
            "not_met": 1, "inconclusive": 1, "not_tested": 1, "evaluated": 3,
            "evaluation_coverage_pct": 60.0, "met_pct_of_evaluated": 66.67,
        })
        self.assertEqual([c["control_id"] for c in payload["controls"]],
                         ["LAB-C001", "LAB-C002", "LAB-C003", "LAB-C004", "LAB-C005"])
        for row in payload["controls"]:
            self.assertEqual(list(row), ["control_id", "title", "criterion", "status", "evidence_id"])
        self.assertEqual(payload["controls"][0]["criterion"], "Synthetic restore exercise records a successful recovery.")

    def test_markdown_report(self):
        result = self.cli("--file", EXAMPLE, "--format", "markdown")
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        self.assertEqual(result.stdout, (GOLDEN / "synthetic-report.md").read_bytes())
        self.assertIn("Synthetic data — not evidence of a real engagement".encode(), result.stdout)
        self.assertIn(b"Statuses are supplied; evidence IDs are labels, not verified artifacts.", result.stdout)

    def test_golden_bytes(self):
        for fmt, ext in (("json", "json"), ("markdown", "md")):
            with self.subTest(fmt=fmt):
                expected = (GOLDEN / ("synthetic-report." + ext)).read_bytes()
                actual = report.render_report(parse_evidence(self.raw), fmt).encode("utf-8")
                result = self.cli("--file", EXAMPLE, "--format", fmt)
                self.assertEqual((result.returncode, result.stderr), (0, b""))
                self.assertEqual(actual, expected)
                self.assertEqual(result.stdout, expected)
                self.assertTrue(actual.endswith(b"\n"))
                self.assertNotIn(b"\r", actual)
                self.assertFalse(actual.startswith(b"\xef\xbb\xbf"))

    def test_deterministic_rendering(self):
        controls = parse_evidence(self.raw)
        for fmt in ("json", "markdown"):
            self.assertEqual(report.render_report(controls, fmt),
                             report.render_report(tuple(reversed(controls)), fmt))

    def test_empty_rendering(self):
        raw = {**self.raw, "controls": []}
        path = self.put(raw)
        result = self.cli("--file", path, "--format", "json")
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        summary = json.loads(result.stdout)["summary"]
        self.assertEqual((summary["total"], summary["omitted"], summary["evaluation_coverage_pct"],
                          summary["met_pct_of_evaluated"]), (0, 5, None, None))
        result = self.cli("--file", path)
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        self.assertIn(b"- evaluation_coverage_pct: N/A\n- met_pct_of_evaluated: N/A\n", result.stdout)
        self.assertTrue(result.stdout.endswith(b"| --- | --- | --- | --- | --- |\n"))

    def test_subset_rendering(self):
        path = self.put({**self.raw, "controls": self.raw["controls"][:1]})
        result = self.cli("--file", path, "--format", "json")
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        summary = json.loads(result.stdout)["summary"]
        self.assertEqual((summary["catalog_total"], summary["total"], summary["omitted"],
                          summary["evaluation_coverage_pct"]), (5, 1, 4, 100.0))
        result = self.cli("--file", path)
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        self.assertIn(b"Coverage is calculated only over submitted controls; omitted catalog controls are not assessed.", result.stdout)
        self.assertIn(b"- evaluation_coverage_pct: 100.00%", result.stdout)

    def test_report_not_input(self):
        path = self.put((GOLDEN / "synthetic-report.json").read_bytes())
        self.assert_error(self.cli("--file", path), 1, "Error: invalid evidence\n")

    def test_input_boundary(self):
        raw = json.dumps(self.raw).encode()
        exact = raw + b" " * (LIMIT - len(raw))
        path = self.put(exact)
        result = self.cli("--file", path)
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        self.assertEqual(result.stdout, (GOLDEN / "synthetic-report.md").read_bytes())
        path.write_bytes(exact + b" ")
        self.assert_error(self.cli("--file", path), 1, "Error: invalid evidence\n")

    def test_invalid_file(self):
        cases = [
            b'{"PRIVATE_MARKER":',
            b'{"schema_version":1,"schema_version":1,"source_kind":"synthetic","controls":[]}',
            b'{"schema_version":1,"source_kind":"synthetic","controls":[{"control_id":"LAB-C001","status":"met","status":"met","evidence_id":"LAB-E001"}]}',
            b"\xff", b"\xef\xbb\xbf" + json.dumps(self.raw).encode(),
            b'{"schema_version":NaN,"source_kind":"synthetic","controls":[]}',
            b'{"schema_version":Infinity,"source_kind":"synthetic","controls":[]}',
            b'{"schema_version":-Infinity,"source_kind":"synthetic","controls":[]}',
            b'{"schema_version":1,"source_kind":"synthetic","controls":[{"control_id":"LAB-C001","status":"met","evidence_id":["LAB-E001"]}]}',
            b"[" * 5000 + b"]" * 5000,
            json.dumps({**self.raw, "extra": "PRIVATE_MARKER"}).encode(),
        ]
        for i, data in enumerate(cases):
            with self.subTest(case=i):
                self.assert_error(self.cli("--file", self.put(data)), 1, "Error: invalid evidence\n")
        for path in (self.directory, self.directory / "missing_PRIVATE_MARKER.json"):
            self.assert_error(self.cli("--file", path), 1, "Error: input unavailable\n")

    def test_input_symlink(self):
        target = self.put(self.raw)
        for destination in (target, self.directory / "missing"):
            link = self.directory / ("link-" + destination.name)
            try:
                link.symlink_to(destination)
            except (OSError, NotImplementedError) as exc:
                self.skipTest("symlink creation unavailable: " + type(exc).__name__)
            self.assert_error(self.cli("--file", link), 1, "Error: input unavailable\n")
            self.assertTrue(link.is_symlink())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO is POSIX-only")
    def test_fifo_rejected(self):
        path = self.directory / "PRIVATE_MARKER.fifo"
        os.mkfifo(path)
        self.assert_error(self.cli("--file", path), 1, "Error: input unavailable\n")

    def test_permission_error(self):
        path = self.put(self.raw)
        out, err = io.StringIO(), io.StringIO()
        with patch.object(Path, "open", side_effect=PermissionError("PRIVATE_MARKER")):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = report.main(["--file", str(path)])
        self.assertEqual((code, out.getvalue(), err.getvalue()), (1, "", "Error: input unavailable\n"))

    def test_invalid_cli(self):
        for args in ((), ("--file",), ("--PRIVATE_MARKER",),
                     ("--file", EXAMPLE, "--format", "PRIVATE_MARKER")):
            with self.subTest(args=args):
                self.assert_error(self.cli(*args), 2, "Error: invalid arguments\n")

    def test_help(self):
        result = self.cli("--help")
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        self.assertIn(b"--file", result.stdout)

    def test_default_format(self):
        default = self.cli("--file", EXAMPLE)
        explicit = self.cli("--file", EXAMPLE, "--format", "markdown")
        self.assertEqual((default.returncode, default.stderr), (0, b""))
        self.assertEqual((explicit.returncode, explicit.stderr), (0, b""))
        self.assertEqual(default.stdout, explicit.stdout)


    def test_new_output(self):
        for fmt in ("markdown", "json"):
            with self.subTest(fmt=fmt):
                path = self.directory / ("report-" + fmt)
                result = self.cli("--file", EXAMPLE, "--format", fmt, "--out", path)
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b"", b""))
                stdout = self.cli("--file", EXAMPLE, "--format", fmt)
                self.assertEqual((stdout.returncode, stdout.stderr), (0, b""))
                self.assertEqual(path.read_bytes(), stdout.stdout)

    def test_existing_output(self):
        path = self.put(b"sentinel", "report.md")
        self.assert_error(self.cli("--file", EXAMPLE, "--out", path), 1, "Error: output unavailable\n")
        self.assertEqual(path.read_bytes(), b"sentinel")

    def test_same_input_output(self):
        path = self.put(self.raw)
        original = path.read_bytes()
        self.assert_error(self.cli("--file", path, "--out", path), 1, "Error: output unavailable\n")
        self.assertEqual(path.read_bytes(), original)

    def test_hardlink_output(self):
        path = self.put(self.raw)
        original = path.read_bytes()
        link = self.directory / "hardlink"
        try:
            os.link(path, link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest("hardlink unavailable: " + type(exc).__name__)
        self.assert_error(self.cli("--file", path, "--out", link), 1, "Error: output unavailable\n")
        self.assertEqual(path.read_bytes(), original)
        self.assertTrue(os.path.samefile(path, link))

    def test_symlink_output(self):
        target = self.put(b"sentinel", "target")
        missing = self.directory / "missing"
        for destination in (target, missing):
            link = self.directory / ("link-" + destination.name)
            try:
                link.symlink_to(destination)
            except (OSError, NotImplementedError) as exc:
                self.skipTest("symlink unavailable: " + type(exc).__name__)
            self.assert_error(self.cli("--file", EXAMPLE, "--out", link), 1, "Error: output unavailable\n")
            self.assertTrue(link.is_symlink())
            self.assertEqual(os.readlink(link), str(destination))
        self.assertEqual(target.read_bytes(), b"sentinel")
        self.assertFalse(missing.exists())

    def test_directory_output(self):
        self.assert_error(self.cli("--file", EXAMPLE, "--out", self.directory), 1, "Error: output unavailable\n")
        self.assertTrue(self.directory.is_dir())

    def test_missing_parent(self):
        path = self.directory / "missing" / "report.md"
        self.assert_error(self.cli("--file", EXAMPLE, "--out", path), 1, "Error: output unavailable\n")
        self.assertFalse(path.parent.exists())

    def test_output_permission_failure(self):
        output = self.directory / "PRIVATE_MARKER"
        real_open = Path.open

        def blocked(path, *args, **kwargs):
            if path == output:
                raise PermissionError("PRIVATE_MARKER")
            return real_open(path, *args, **kwargs)

        out, err = io.StringIO(), io.StringIO()
        with patch.object(Path, "open", blocked):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = report.main(["--file", str(EXAMPLE), "--out", str(output)])
        self.assertEqual((code, out.getvalue(), err.getvalue()), (1, "", "Error: output unavailable\n"))
        self.assertFalse(output.exists())

    def test_write_failure_no_unlink(self):
        sentinel = self.put(b"unchanged", "sentinel")
        real_open = Path.open

        class FailedStream:
            def __init__(self, stream, fail_on_close):
                self.stream = stream
                self.fail_on_close = fail_on_close

            def __enter__(self):
                return self

            def write(self, data):
                if self.fail_on_close:
                    return self.stream.write(data)
                self.stream.write(data[:7])
                raise OSError("PRIVATE_MARKER")

            def __exit__(self, *args):
                self.stream.close()
                if self.fail_on_close:
                    raise OSError("PRIVATE_MARKER")

        for fail_on_close in (False, True):
            with self.subTest(close=fail_on_close):
                output = self.directory / ("failed-" + str(fail_on_close))

                def failing_open(path, *args, **kwargs):
                    stream = real_open(path, *args, **kwargs)
                    return FailedStream(stream, fail_on_close) if path == output else stream

                out, err = io.StringIO(), io.StringIO()
                with patch.object(Path, "open", failing_open), \
                        patch.object(Path, "unlink", side_effect=AssertionError("must not unlink")), \
                        patch.object(os, "unlink", side_effect=AssertionError("must not unlink")):
                    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                        code = report.main(["--file", str(EXAMPLE), "--out", str(output)])
                self.assertEqual((code, out.getvalue(), err.getvalue()),
                                 (1, "", "Error: output unavailable\n"))
                self.assertTrue(output.is_file())
                expected = (GOLDEN / "synthetic-report.md").read_bytes()
                self.assertEqual(output.read_bytes(), expected if fail_on_close else expected[:7])
                self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def test_invalid_input_does_not_create_output(self):
        output = self.directory / "new-report.md"
        path = self.put(b'{"invalid":true}')
        self.assert_error(self.cli("--file", path, "--out", output), 1, "Error: invalid evidence\n")
        self.assertFalse(output.exists())
