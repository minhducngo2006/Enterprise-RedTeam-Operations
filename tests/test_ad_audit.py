#!/usr/bin/env python3
"""
Unit tests for Active Directory Attack Surface Analyzer (ad_audit)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))
from ad_audit import UACParser, ActiveDirectoryAuditor

class TestADAudit(unittest.TestCase):

    def test_uac_parser_normal_account(self):
        """Verify normal account (512 / 0x200) flags."""
        res = UACParser.parse(512)
        self.assertEqual(res["uac_hex"], "0x200")
        self.assertFalse(res["is_disabled"])
        self.assertFalse(res["is_asrep_roastable"])
        self.assertEqual(res["risk_level"], "LOW")

    def test_uac_parser_asrep_roastable(self):
        """Verify DONT_REQ_PREAUTH flag (0x400000) detection."""
        # 0x400000 (DONT_REQ_PREAUTH) + 0x200 (NORMAL_ACCOUNT) = 4194816
        res = UACParser.parse(4194816)
        self.assertTrue(res["is_asrep_roastable"])
        self.assertEqual(res["risk_level"], "HIGH")

    def test_kerberoasting_evaluation(self):
        """Verify service account with SPN is flagged for Kerberoasting."""
        account = {
            "sAMAccountName": "svc_sql",
            "servicePrincipalNames": ["MSSQLSvc/sql01:1433"],
            "adminCount": 1
        }
        res = ActiveDirectoryAuditor.evaluate_spn(account)
        self.assertIsNotNone(res)
        self.assertEqual(res["account"], "svc_sql")
        self.assertEqual(res["risk"], "HIGH")
        self.assertEqual(res["tier"], "Tier 0 / Privileged")

    def test_machine_account_spn_ignored(self):
        """Verify computer accounts ($) are not flagged as standard Kerberoast targets."""
        account = {
            "sAMAccountName": "DC01$",
            "servicePrincipalNames": ["HOST/DC01.corp.local"]
        }
        res = ActiveDirectoryAuditor.evaluate_spn(account)
        self.assertIsNone(res)

if __name__ == "__main__":
    unittest.main()
