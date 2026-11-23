# Red Team Operations Engagement Final Report

## Document Classification: Strictly Confidential (Sanitized)
- **Target Organization**: Global Enterprise Infrastructure (Sanitized)
- **Assessment Scope**: Full-Scope Adversary Emulation & Kill Chain Exercise
- **Execution Period**: 14 Days
- **Assessment Standard**: MITRE ATT&CK Framework
- **Overall Posture Rating**: **HIGH RISK / CROWN JEWELS COMPROMISED**

---

## 1. Executive Summary

A simulated full-scope adversary emulation exercise was conducted against the target enterprise. The objective of the exercise was to evaluate the organization's defensive posture, validate SOC / Blue Team detection capabilities, and assess the feasibility of an external threat actor breaching the perimeter, moving laterally, and exfiltrating critical business assets (Finance & Customer ERP records).

### Key Findings & Outcomes:
1. **Perimeter Breach**: Initial access was obtained via a spear-phishing campaign deploying an ISO container with an obfuscated LNK shortcut, completely bypassing perimeter email gateways and Mark-of-the-Web (MOTW) controls.
2. **Endpoint Evasion**: In-memory payload loaders successfully unhooked user-mode `ntdll.dll` functions and patched AMSI memory space, establishing encrypted HTTPS C2 communication with zero alerts triggered on the deployed EDR solution.
3. **Privilege Escalation & Domain Dominance**: By performing Kerberoasting against a high-privilege service account (`svc_mssql_prod`) and exploiting Active Directory Certificate Services (AD CS - ESC1), the Red Team obtained full Domain Administrator privileges within 72 hours of initial access.
4. **Crown Jewels Compromised**: Successfully accessed the production database cluster, obtaining administrative access to over 1.2 million customer financial records, and simulated exfiltration via encrypted C2 channels.

### Attack Timeline Summary

| Phase | Duration | Operational Milestone |
| :--- | :--- | :--- |
| **Reconnaissance** | Day 1-2 | OSINT, infrastructure staging, C2 redirectors deployed |
| **Initial Access** | Day 3 | Phishing payload delivered; foothold established on Workstation WS-0419 |
| **Evasion & Discovery** | Day 4-5 | In-memory EDR evasion; internal AD enumeration via BloodHound |
| **Credential Access** | Day 6 | Kerberoasting executed; svc_mssql_prod hash recovered and cracked |
| **Lateral Movement** | Day 7 | Lateral movement to SQL Cluster; pivoted across internal VLANs |
| **Domain Dominance** | Day 8 | AD CS ESC1 certificate request; Domain Administrator impersonation |
| **Crown Jewels Action** | Day 9-11 | Full Domain Controller compromise; ERP customer database dumped |
| **Closure & Remediation**| Day 12-14 | Deconfliction with Blue Team, artifact cleanup, remediation alignment |

---

## 2. MITRE ATT&CK Execution Matrix

| Tactic | Technique ID | Technique Name | Operational Implementation |
| :--- | :--- | :--- | :--- |
| **Reconnaissance** | T1592 | Gather Victim Host Info | Passive OSINT via certificate logs and public code repositories |
| **Initial Access** | T1566.001 | Spear-Phishing Attachment | Delivered ISO container with embedded LNK and DLL payload |
| **Execution** | T1204.002 | User Execution | Victim mounted ISO and executed malicious shortcut |
| **Defense Evasion**| T1562.001 | Impair Defenses | Memory patching of `amsi.dll` and dynamic clean NTDLL mapping |
| **Credential Access**| T1558.003 | Kerberoasting | Requested TGS tickets for accounts configured with SPNs |
| **Discovery** | T1087.002 | Domain Account Discovery | Targeted LDAP queries mapped Active Directory attack paths |
| **Lateral Movement**| T1021.002 | SMB / Named Pipes | Executed fileless commands across systems via WinRM and WMI |
| **Privilege Escalation**| T1649 | Steal or Forge Auth Certs | Exploited misconfigured AD CS certificate template (ESC1) |
| **Exfiltration** | T1041 | Exfiltration Over C2 | Staged encrypted records transmitted over HTTPS C2 channel |

---

## 3. Detailed Technical Narrative

### Phase 1: Initial Access & Endpoint Foothold
The Red Team staged external infrastructure utilizing Amazon Web Services (AWS) redirectors configured with valid SSL certificates. 

A spear-phishing email disguised as an executive quarterly bonus review was sent to a targeted distribution list. The email contained an ISO container file (`Bonus_Review_2026.iso`). When mounted, the user executed an LNK file that triggered an in-memory reflective DLL loader. The payload performed AMSI unhooking, restored clean `ntdll.dll` syscall stubs, and connected back to the C2 team server over port 443 with randomized sleep jitter (60s ± 30%).

### Phase 2: Internal Discovery & Kerberoasting
Operating from workstation `WS-0419` under standard user context `j_smith`:
1. Targeted LDAP queries identified service accounts with ServicePrincipalNames (SPNs).
2. Identified `svc_mssql_prod` which possessed `AdminCount = 1` and belonged to the `Database Admins` security group.
3. A TGS ticket was requested using standard Kerberos API calls. Because RC4-HMAC (`etype 23`) encryption was enabled on the account, the ticket hash was recovered and cracked offline in 3 hours using a common dictionary attack, revealing the plaintext password: `Winter2025!`.

### Phase 3: Domain Dominance via AD CS (ESC1)
With administrative access to the database cluster, the Red Team mapped Active Directory Certificate Services (AD CS):
1. Discovered an enterprise certificate template (`WebServer-ClientAuth`) that had `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` enabled and allowed enrollment by `Domain Users`.
2. Using the initial user context, requested a certificate specifying `administrator@corp.local` in the Subject Alternative Name (SAN).
3. The certificate authority issued a valid PKCS#12 certificate.
4. Used the certificate to authenticate against the Domain Controller (`DC01.corp.local`) via PKINIT Kerberos authentication, obtaining the Domain Administrator NTLM hash.

### Phase 4: Crown Jewels Compromise
Using the Domain Administrator credentials:
1. Connected to `DC01` via WinRM (port 5985).
2. Extracted the `krbtgt` account hash to verify persistence capability.
3. Authenticated to the primary Finance ERP database (`SQL-FIN-01`).
4. Dumped table schemas and verified read access to 1.2 million customer billing records.

---

## 4. Blue Team & SOC Detection Scorecard

| Phase | Observed Alert Status | SOC Detection Analysis |
| :--- | :--- | :--- |
| **Phishing Email Delivery** | **Passed Undetected** | Email gateway failed to inspect ISO container contents. |
| **In-Memory EDR Execution** | **Bypassed** | AMSI patching and indirect syscalls eliminated process telemetry hooks. |
| **LDAP Reconnaissance** | **Undetected** | Paged LDAP queries blended with normal domain controller traffic. |
| **Kerberoasting** | **Partially Alerted** | Event ID 4769 logged, but correlation rule was not configured to trigger an analyst alert. |
| **AD CS Certificate Enrollment** | **Undetected** | Security logs did not monitor certificate template SAN alterations. |
| **Domain Admin Remote Login** | **Alert Triggered (Day 9)**| Admin login from an unrecognized workstation triggered an anomaly alert (18 hours after occurrence). |

---

## 5. Strategic Defense & Hardening Roadmap

### 1. Active Directory & Identity Hygiene
* **Deploy Group Managed Service Accounts (gMSA)**: Migrate all service accounts (specifically `svc_mssql_prod`) to gMSAs to enforce automatic 120-character password rotation.
* **Harden Active Directory Certificate Services**: Revoke `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` on all templates where `Client Authentication` EKU is enabled; restrict enrollment to dedicated security groups with manager approval required.
* **Enforce Tiered Administration Model (Tier 0 / Tier 1 / Tier 2)**: Prevent Domain Admins from logging into standard Tier 2 workstations where credentials can be harvested.

### 2. Endpoint & Network Telemetry
* **Enable Attack Surface Reduction (ASR) Rules**: Block child processes spawned from Office/script interpreters and enforce blocking of untrusted executables in container files.
* **Configure SIEM Correlation for Kerberoasting**: Create high-priority alerts for Windows Event ID 4769 when `Ticket Options` contains `0x40810000` and `Ticket Encryption Type` is `0x17` (RC4) requested by non-service accounts.
