#!/usr/bin/env python3
"""
Unit tests for the scalar UserAccountControl decoder (ad_audit)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))
from ad_audit import UACParser

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

if __name__ == "__main__":
    unittest.main()
