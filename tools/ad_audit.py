#!/usr/bin/env python3
"""Standalone educational UserAccountControl bitmask decoder."""

import argparse
import json
import os
import sys
from typing import Any, Dict

# ANSI Colors
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"

    @classmethod
    def disable(cls):
        cls.RESET = cls.BOLD = cls.RED = cls.GREEN = cls.YELLOW = ""
        cls.BLUE = cls.MAGENTA = cls.CYAN = cls.GRAY = ""

if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    Color.disable()

# UserAccountControl (UAC) Flag Definitions (MS-SAMR / Active Directory)
UAC_FLAGS = {
    0x0001: ("SCRIPT", "Logon script executed"),
    0x0002: ("ACCOUNTDISABLE", "Account is disabled"),
    0x0008: ("HOMEDIR_REQUIRED", "Home directory required"),
    0x0010: ("LOCKOUT", "Account locked out"),
    0x0020: ("PASSWD_NOTREQD", "No password required (High Risk)"),
    0x0040: ("PASSWD_CANT_CHANGE", "Cannot change password"),
    0x0080: ("ENCRYPTED_TEXT_PWD_ALLOWED", "Encrypted password permitted"),
    0x0100: ("TEMP_DUPLICATE_ACCOUNT", "Temporary duplicate account"),
    0x0200: ("NORMAL_ACCOUNT", "Default standard user account"),
    0x0800: ("INTERDOMAIN_TRUST_ACCOUNT", "Interdomain trust account"),
    0x1000: ("WORKSTATION_TRUST_ACCOUNT", "Computer / Workstation account"),
    0x2000: ("SERVER_TRUST_ACCOUNT", "Domain Controller account"),
    0x10000: ("DONT_EXPIRE_PASSWORD", "Password never expires (Hygiene Risk)"),
    0x20000: ("MNS_LOGON_ACCOUNT", "MNS logon account"),
    0x40000: ("SMARTCARD_REQUIRED", "Smartcard required for logon"),
    0x80000: ("TRUSTED_FOR_DELEGATION", "Unconstrained Kerberos Delegation (Critical Risk)"),
    0x100000: ("NOT_DELEGATED", "Account cannot be delegated"),
    0x200000: ("USE_DES_KEY_ONLY", "Restricted to weak DES encryption"),
    0x400000: ("DONT_REQ_PREAUTH", "Kerberos Pre-Authentication Not Required (AS-REP Roastable)"),
    0x800000: ("PASSWORD_EXPIRED", "Password expired"),
    0x1000000: ("TRUSTED_TO_AUTH_FOR_DELEGATION", "Constrained Delegation with Protocol Transition (High Risk)")
}

class UACParser:
    """Decodes integer UserAccountControl bitmasks into human-readable flags and risk scores."""

    @staticmethod
    def parse(uac_value: int) -> Dict[str, Any]:
        matched_flags = []
        is_asrep_roastable = bool(uac_value & 0x400000)
        is_unconstrained_delegation = bool(uac_value & 0x80000)
        is_pwd_not_required = bool(uac_value & 0x0020)
        is_disabled = bool(uac_value & 0x0002)

        for mask, (flag_name, desc) in UAC_FLAGS.items():
            if uac_value & mask:
                matched_flags.append({"mask": hex(mask), "flag": flag_name, "description": desc})

        risk_level = "LOW"
        if is_unconstrained_delegation:
            risk_level = "CRITICAL"
        elif is_asrep_roastable or is_pwd_not_required:
            risk_level = "HIGH"

        return {
            "uac_integer": uac_value,
            "uac_hex": hex(uac_value),
            "is_disabled": is_disabled,
            "is_asrep_roastable": is_asrep_roastable,
            "is_unconstrained_delegation": is_unconstrained_delegation,
            "is_password_not_required": is_pwd_not_required,
            "risk_level": risk_level,
            "flags": matched_flags
        }

class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "Error: invalid arguments\n")


def _parse_uac_mask(value):
    if not (1 <= len(value) <= 10 and value.isascii() and value.isdecimal()):
        raise argparse.ArgumentTypeError("invalid mask")
    mask = int(value)
    if mask > 4294967295:
        raise argparse.ArgumentTypeError("invalid mask")
    return mask


def main():
    parser = _SafeArgumentParser(
        description="Educational UserAccountControl bitmask decoder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python3 ad_audit.py uac 512 --json"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: uac
    p_uac = subparsers.add_parser("uac", help="Decode UserAccountControl integer mask")
    p_uac.add_argument("mask", type=_parse_uac_mask, help="UserAccountControl decimal integer (e.g., 512, 66048, 4194816)")
    p_uac.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if not args.command:
        parser.error("missing command")

    if not (args.command == "uac" and args.json):
        print(f"{Color.CYAN}{Color.BOLD}[*] UserAccountControl bitmask decoder{Color.RESET}")

    if args.command == "uac":
        result = UACParser.parse(args.mask)
        if args.json:
            print(json.dumps(result, indent=2))
            return

        risk_color = Color.RED if result["risk_level"] == "CRITICAL" else Color.YELLOW if result["risk_level"] == "HIGH" else Color.GREEN
        print(f"\n{Color.BOLD}UAC Mask: {result['uac_integer']} ({result['uac_hex']}){Color.RESET}")
        print(f"Risk Rating: {risk_color}{result['risk_level']}{Color.RESET}")
        print(f"Account Disabled: {result['is_disabled']}")
        print(f"AS-REP Roastable (Pre-Auth Disabled): {result['is_asrep_roastable']}")
        print(f"Unconstrained Delegation: {result['is_unconstrained_delegation']}")
        print(f"\n{Color.BOLD}Identified Bitflags:{Color.RESET}")
        for f in result["flags"]:
            print(f"  - [{f['mask']}] {Color.BOLD}{f['flag']}{Color.RESET}: {f['description']}")

if __name__ == "__main__":
    main()
