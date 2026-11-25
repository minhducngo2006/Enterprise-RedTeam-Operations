import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "ad_audit.py"


class TestUacCli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args],
            capture_output=True, text=True, timeout=10, check=False,
        )

    def test_json_stdout_is_document(self):
        result = self.run_cli("uac", "512", "--json")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["uac_integer"], 512)
        self.assertEqual(payload["uac_hex"], "0x200")

    def test_plain_output(self):
        result = self.run_cli("uac", "512")
        self.assertEqual(result.returncode, 0)
        self.assertIn("0x200", result.stdout)


    def test_invalid_mask(self):
        for mask in ("-1", "4294967296", "not-int", "５１２", "+1",
                     " 512", "512 ", "00000000512", "PRIVATE_MARKER"):
            with self.subTest(mask=mask):
                result = self.run_cli("uac", mask, "--json")
                self.assertEqual((result.returncode, result.stdout, result.stderr),
                                 (2, "", "Error: invalid arguments\n"))

    def test_mask_boundaries(self):
        for mask, expected in (("0", 0), ("4294967295", 4294967295),
                               ("0000000512", 512)):
            with self.subTest(mask=mask):
                result = self.run_cli("uac", mask, "--json")
                self.assertEqual((result.returncode, result.stderr), (0, ""))
                self.assertEqual(json.loads(result.stdout)["uac_integer"], expected)

    def test_help(self):
        result = self.run_cli("uac", "--help")
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertIn("mask", result.stdout)

    def test_bad_option(self):
        result = self.run_cli("uac", "512", "--PRIVATE_MARKER")
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, "", "Error: invalid arguments\n"))


    def test_legacy_command_retired(self):
        result = self.run_cli("analyze")
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, "", "Error: invalid arguments\n"))
        result = self.run_cli("--help")
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertIn("{uac}", result.stdout)
        self.assertNotIn("analyze", result.stdout)


if __name__ == "__main__":
    unittest.main()
