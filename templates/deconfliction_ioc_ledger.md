# Red Team Activity & Deconfliction IOC Ledger

This ledger records all red team activities, operational timestamps, compromised hosts, staging directories, and artifact cleanup verifications.

| Timestamp (UTC) | Source IP / C2 | Target Host | Executed Technique | Account Context | Artifact Created | Cleanup Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-03-03 14:15 | `198.51.100.42` | `WS-0419` | Phishing Payload / C2 Beacon | `CORP\j_smith` | Memory Only (In-process) | Terminated |
| 2026-03-05 09:30 | `10.10.20.15` | `DC01` | Kerberoast TGS Request | `CORP\j_smith` | Event ID 4769 logged | N/A (Standard Auth) |
| 2026-03-07 11:20 | `10.10.20.15` | `SQL-01` | WinRM Lateral Movement | `CORP\svc_mssql_prod` | WinRM Session Event 91 | Disconnected |
| 2026-03-08 16:45 | `10.10.20.15` | `CORP-CA` | AD CS ESC1 Certificate Req | `CORP\j_smith` | Certificate Serial `4A82F0` | Revoked by Admin |
| 2026-03-10 10:00 | `10.10.10.5` | `DC01` | WinRM Remote Execution | `CORP\Administrator` | Event 4624 (Logon Type 3) | Session Cleared |

---

## Artifact Removal Verification Checklist
- [x] All active C2 beacon agents terminated and memory unmapped.
- [x] Temporary staging directories and test files removed from all endpoints.
- [x] Test certificates requested from AD CS revoked in the Certificate Authority console.
- [x] Group Policy modifications reverted to baseline configuration.
- [x] White Cell verification and deconfliction confirmation received.
