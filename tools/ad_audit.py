#!/usr/bin/env python3
"""
ad_audit - Active Directory Attack Surface & Kerberos Attack Path Analyzer
Evaluates Active Directory configurations, UserAccountControl bitflags,
Kerberoasting SPN exposure, and AS-REP roasting vectors.
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

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

class ActiveDirectoryAuditor:
    """Analyzes Active Directory objects for privilege escalation and credential access vectors."""

    @staticmethod
    def evaluate_spn(user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluates whether an account is vulnerable to Kerberoasting."""
        spns = user.get("servicePrincipalNames", []) or user.get("spns", [])
        if not spns:
            return None

        # Ignore machine accounts ending in $ unless specified
        sam_name = user.get("sAMAccountName", "") or user.get("name", "")
        if sam_name.endswith("$"):
            return None

        admin_count = bool(user.get("adminCount", 0))
        tier = "Tier 0 / Privileged" if admin_count else "Tier 1 / Standard Service"
        
        return {
            "account": sam_name,
            "distinguishedName": user.get("distinguishedName", ""),
            "spns": spns,
            "adminCount": admin_count,
            "tier": tier,
            "risk": "HIGH" if admin_count else "MEDIUM",
            "attack_vector": "Kerberoasting (T1558.003)",
            "mitigation": "Enforce managed service accounts (gMSA) or AES256 passwords >= 25 characters."
        }

    @staticmethod
    def evaluate_asrep(user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluates whether an account can be attacked via AS-REP Roasting."""
        uac = user.get("userAccountControl", 0)
        if isinstance(uac, str):
            try:
                uac = int(uac)
            except ValueError:
                uac = 0

        parsed_uac = UACParser.parse(uac)
        if parsed_uac["is_asrep_roastable"] and not parsed_uac["is_disabled"]:
            sam_name = user.get("sAMAccountName", "") or user.get("name", "")
            return {
                "account": sam_name,
                "uac": uac,
                "uac_hex": parsed_uac["uac_hex"],
                "risk": "HIGH",
                "attack_vector": "AS-REP Roasting (T1558.004)",
                "description": "Pre-authentication disabled. An attacker can request an encrypted AS-REP ticket without authentication and crack it offline.",
                "mitigation": "Enable 'Do not require Kerberos preauthentication' requirement in Active Directory Users & Computers."
            }
        return None

    @classmethod
    def audit_dataset(cls, accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        kerberoastable = []
        asrep_roastable = []
        unconstrained_delegation = []

        for acc in accounts:
            spn_finding = cls.evaluate_spn(acc)
            if spn_finding:
                kerberoastable.append(spn_finding)

            asrep_finding = cls.evaluate_asrep(acc)
            if asrep_finding:
                asrep_roastable.append(asrep_finding)

            uac = acc.get("userAccountControl", 0)
            if isinstance(uac, int) and (uac & 0x80000) and not (uac & 0x0002):
                unconstrained_delegation.append({
                    "account": acc.get("sAMAccountName", "") or acc.get("name", ""),
                    "risk": "CRITICAL",
                    "attack_vector": "Unconstrained Delegation (T1558.001)",
                    "description": "Server can impersonate any connecting user across the forest, including Domain Admins."
                })

        return {
            "total_accounts_analyzed": len(accounts),
            "kerberoastable_candidates": kerberoastable,
            "asrep_roastable_candidates": asrep_roastable,
            "unconstrained_delegation_candidates": unconstrained_delegation
        }

def generate_markdown_report(audit_data: Dict[str, Any]) -> str:
    """Generates a technical Active Directory attack surface report."""
    kb_count = len(audit_data["kerberoastable_candidates"])
    asrep_count = len(audit_data["asrep_roastable_candidates"])
    delegation_count = len(audit_data["unconstrained_delegation_candidates"])

    report = f"""# Active Directory Assessment & Credential Attack Surface Report

## 1. Executive Summary
- **Evaluation Date**: {datetime.now().strftime("%Y-%m-%d")}
- **Total Accounts Analyzed**: {audit_data["total_accounts_analyzed"]}
- **Kerberoastable Service Accounts Identified**: {kb_count}
- **AS-REP Roastable Accounts (Pre-Auth Disabled)**: {asrep_count}
- **Unconstrained Delegation Exposure**: {delegation_count}

---

## 2. Kerberoasting Exposure (T1558.003)
Kerberoasting allows standard authenticated domain users to request Ticket Granting Service (TGS) tickets for accounts configured with Service Principal Names (SPNs) and crack the service account NTLM hashes offline.

| Account Name | Administrative Tier | Associated SPNs | Risk Level |
| :--- | :--- | :--- | :--- |
"""
    for kb in audit_data["kerberoastable_candidates"]:
        spn_str = "<br/>".join(kb["spns"][:2])
        report += f"| `{kb['account']}` | {kb['tier']} | `{spn_str}` | **{kb['risk']}** |\n"

    report += """
---

## 3. AS-REP Roasting Exposure (T1558.004)
Accounts with Kerberos Pre-Authentication disabled (`DONT_REQ_PREAUTH`) allow any unauthenticated or low-privileged entity to request an encrypted AS-REP response directly from the KDC.

| Account Name | UAC Flag Hex | Primary Risk | Mitigation |
| :--- | :--- | :--- | :--- |
"""
    for asrep in audit_data["asrep_roastable_candidates"]:
        report += f"| `{asrep['account']}` | `{asrep['uac_hex']}` | Pre-Auth Disabled | Enforce Kerberos Pre-Authentication |\n"

    report += """
---

## 4. Remediation & Hardening Roadmap
1. **Transition to Group Managed Service Accounts (gMSA)**: Automatically rotates complex 120-character passwords, completely eliminating Kerberoasting risks.
2. **Disable Weak Encryption (RC4)**: Enforce AES-128 and AES-256 for Kerberos tickets to make offline hash cracking computationally infeasible.
3. **Audit UserAccountControl Flags**: Periodically scan for `DONT_REQ_PREAUTH` and `TRUSTED_FOR_DELEGATION` across the directory tree.
"""
    return report

def main():
    parser = argparse.ArgumentParser(
        description="Active Directory Attack Path & Kerberos Exposure Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 ad_audit.py uac 4194816
  python3 ad_audit.py analyze --file ad_users.json --report
  python3 ad_audit.py analyze --demo --out ad_assessment.md
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: uac
    p_uac = subparsers.add_parser("uac", help="Decode UserAccountControl integer mask")
    p_uac.add_argument("mask", type=int, help="UserAccountControl decimal integer (e.g., 512, 66048, 4194816)")
    p_uac.add_argument("--json", action="store_true", help="Output in JSON format")

    # Command: analyze
    p_an = subparsers.add_parser("analyze", help="Analyze Active Directory JSON account exports")
    p_an.add_argument("--file", help="Path to Active Directory JSON export (BloodHound or LDAP dump)")
    p_an.add_argument("--demo", action="store_true", help="Run analysis against built-in enterprise sample dataset")
    p_an.add_argument("--report", action="store_true", help="Print formatted markdown report")
    p_an.add_argument("--out", help="Write report to file path")
    p_an.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    print(f"{Color.CYAN}{Color.BOLD}[*] Active Directory Attack Path Analyzer v1.0.0{Color.RESET}")

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

    elif args.command == "analyze":
        dataset = []
        if args.demo:
            dataset = [
                {
                    "sAMAccountName": "svc_mssql_prod",
                    "distinguishedName": "CN=svc_mssql_prod,OU=ServiceAccounts,DC=corp,DC=local",
                    "servicePrincipalNames": ["MSSQLSvc/sql01.corp.local:1433", "MSSQLSvc/sql01.corp.local"],
                    "userAccountControl": 66048,
                    "adminCount": 1
                },
                {
                    "sAMAccountName": "svc_backup_exec",
                    "distinguishedName": "CN=svc_backup_exec,OU=ServiceAccounts,DC=corp,DC=local",
                    "servicePrincipalNames": ["BACKUP/backup01.corp.local"],
                    "userAccountControl": 512,
                    "adminCount": 0
                },
                {
                    "sAMAccountName": "j_doe_legacy",
                    "distinguishedName": "CN=John Doe,OU=Contractors,DC=corp,DC=local",
                    "servicePrincipalNames": [],
                    "userAccountControl": 4194816,  # DONT_REQ_PREAUTH (0x400000)
                    "adminCount": 0
                },
                {
                    "sAMAccountName": "fs01$",
                    "distinguishedName": "CN=FS01,OU=Domain Controllers,DC=corp,DC=local",
                    "servicePrincipalNames": ["HOST/fs01.corp.local"],
                    "userAccountControl": 593920,   # TRUSTED_FOR_DELEGATION (0x80000)
                    "adminCount": 1
                },
                {
                    "sAMAccountName": "standard_user",
                    "distinguishedName": "CN=Standard User,OU=Users,DC=corp,DC=local",
                    "servicePrincipalNames": [],
                    "userAccountControl": 512,
                    "adminCount": 0
                }
            ]
        elif args.file:
            if not os.path.isfile(args.file):
                print(f"{Color.RED}[-] File not found: {args.file}{Color.RESET}")
                sys.exit(1)
            with open(args.file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                # Handle bloodhound format vs flat array
                dataset = raw_data.get("users", raw_data) if isinstance(raw_data, dict) else raw_data

        if not dataset:
            print(f"{Color.YELLOW}[!] No accounts provided. Use --demo or --file <path>{Color.RESET}")
            sys.exit(1)

        audit_results = ActiveDirectoryAuditor.audit_dataset(dataset)

        if args.json:
            print(json.dumps(audit_results, indent=2))
            return

        kb_count = len(audit_results["kerberoastable_candidates"])
        asrep_count = len(audit_results["asrep_roastable_candidates"])
        delegation_count = len(audit_results["unconstrained_delegation_candidates"])

        print(f"\n{Color.BOLD}Analysis Summary ({len(dataset)} Accounts):{Color.RESET}")
        print(f"  - Kerberoastable SPN Accounts: {Color.RED if kb_count else Color.GREEN}{kb_count}{Color.RESET}")
        print(f"  - AS-REP Roastable (No Pre-Auth): {Color.RED if asrep_count else Color.GREEN}{asrep_count}{Color.RESET}")
        print(f"  - Unconstrained Delegation: {Color.RED if delegation_count else Color.GREEN}{delegation_count}{Color.RESET}")

        if kb_count > 0:
            print(f"\n{Color.YELLOW}[!] High-Value Kerberoasting Targets:{Color.RESET}")
            for target in audit_results["kerberoastable_candidates"]:
                print(f"    * Account: {Color.BOLD}{target['account']}{Color.RESET} [{target['tier']}]")
                for s in target["spns"]:
                    print(f"      └── SPN: {s}")

        if asrep_count > 0:
            print(f"\n{Color.YELLOW}[!] AS-REP Roastable Accounts (Offline Hash Recovery):{Color.RESET}")
            for target in audit_results["asrep_roastable_candidates"]:
                print(f"    * Account: {Color.BOLD}{target['account']}{Color.RESET} (UAC: {target['uac_hex']})")

        if args.report or args.out:
            report_md = generate_markdown_report(audit_results)
            if args.out:
                with open(args.out, "w", encoding="utf-8") as f:
                    f.write(report_md)
                print(f"\n{Color.GREEN}[✓] Technical report exported to: {args.out}{Color.RESET}")
            else:
                print("\n" + report_md)

if __name__ == "__main__":
    main()
