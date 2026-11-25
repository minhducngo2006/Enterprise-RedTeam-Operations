# Rules of Engagement — Defensive Assessment Template

> **TEMPLATE ONLY — NOT AN AUTHORIZATION**
>
> This document is a planning template. It does not grant permission to access, scan, test, alter or monitor any system. No activity is authorized until the applicable organization has separately approved a complete scope in writing through its authorized process and the relevant owners have confirmed the test window. This template does not create legal immunity, a safe harbor or protection from disciplinary action.

## 1. Assessment identity

| Field | Value |
|---|---|
| Engagement / exercise ID | `[REQUIRED — UNASSIGNED]` |
| Assessment title | `[REQUIRED]` |
| Organization / legal entity | `[REQUIRED — OWNER TO COMPLETE]` |
| Business owner | `[REQUIRED — NAME / ROLE]` |
| Security owner | `[REQUIRED — NAME / ROLE]` |
| Technical lead | `[REQUIRED — NAME / ROLE]` |
| Document version | `[REQUIRED]` |
| Status | `DRAFT — NOT AUTHORIZED` |
| Approval date (UTC) | `[BLANK UNTIL APPROVED]` |

## 2. Objective and permitted assessment scope

Describe the defensive objective, the control being assessed and the expected evidence. For the V2.1 portfolio, the fixed control catalog is:

- LAB-C001 — Backup Restoration
- LAB-C002 — Alert Triage
- LAB-C003 — Patch Review
- LAB-C004 — Access Review
- LAB-C005 — Incident Escalation

| Scope item | Explicit value required |
|---|---|
| In-scope environment | `[EXACT SYSTEM / TENANT / LAB IDENTIFIERS]` |
| In-scope controls | `[CONTROL IDS]` |
| Out-of-scope assets / tenants | `[EXPLICIT LIST]` |
| Allowed data | `[SYNTHETIC FIXTURES ONLY; NO REAL ENVIRONMENT OR DATA]` |
| Allowed validation methods | `[READ-ONLY REVIEW OF SYNTHETIC FIXTURES / PAPER TABLETOP USING SYNTHETIC FIXTURES ONLY]` |
| Start and end (UTC) | `[APPROVED WINDOW]` |
| Source locations | `[SYNTHETIC FIXTURE PATHS ONLY; NO LIVE LOG SOURCES]` |

Do not use wildcard scope. Identify each environment and its owner. Any ambiguous asset is out of scope until explicitly added through a separately approved change.

## 3. Prohibited activity

For this project and its synthetic-only evidence toolkit, the following are prohibited:

- live scanning, probing or testing of any real system as part of this synthetic-only portfolio;
- vendor-run or live simulations, even when described as benign;
- credential harvesting, password/hash collection or credential testing;
- endpoint-evasion, security-control tampering or bypass instructions;
- persistence, lateral movement, command-and-control or remote execution;
- access to, copying or exfiltration of real customer or personal data;
- modification of production systems, accounts, policies or security settings;
- testing outside the written scope or approved window.

Any broader activity requires a separate project, risk review and explicit authorization; it is not implied by this template.

## 4. Safety controls and stop conditions

Stop the activity and preserve only the synthetic exercise record. If real sensitive data or an actual incident is encountered, stop collection and route it through the organization's incident-response process; do not copy raw logs or data into this repository. Notify the designated owner if any of the following occurs:

- an asset, tenant, identity or dataset is outside the approved scope;
- service availability, integrity or confidentiality may be affected;
- real credentials, personal data or customer records are encountered;
- a control behaves unexpectedly or an alert indicates possible real compromise;
- the activity cannot be safely distinguished from an actual incident;
- an authorized contact requests a stop;
- the approved window expires or a required contact is unavailable.

| Stop authority | Contact / role | Approved communication channel |
|---|---|---|
| Business owner | `[BLANK]` | `[BLANK]` |
| Security incident owner | `[BLANK]` | `[BLANK]` |
| Technical lead | `[BLANK]` | `[BLANK]` |

No contact is pre-filled or presumed available.

## 5. Data handling and evidence

- Repository examples and fixtures must be synthetic.
- Do not place secrets, personal data, customer records, raw directory exports, production logs or host inventories in this repository.
- Record a source type, control ID, evidence reference label, collection method, timestamp and reviewer for every assessment record.
- An evidence reference label is not the artifact itself and is not proof of integrity.
- Store any real engagement evidence only in the organization's approved restricted evidence repository, outside this project.
- Define access, retention, deletion and incident escalation before collecting any data.

## 6. Deconfliction and communication

Record the approved owner, communication channel, escalation route and change-control process. A deconfliction record does not expand the approved scope. Unexpected indicators of a real incident must be routed to the organization's incident-response process, not treated as exercise success.

## 7. Approval record

All approvals must be completed through the organization's approved signing process. A typed placeholder or an unsigned copy is not authorization.

| Approver role | Name / identity | Decision | Approval reference | Timestamp (UTC) |
|---|---|---|---|---|
| Business owner | `[BLANK]` | `PENDING` | `[BLANK]` | `[BLANK]` |
| Security owner | `[BLANK]` | `PENDING` | `[BLANK]` | `[BLANK]` |
| System / data owner | `[BLANK]` | `PENDING` | `[BLANK]` | `[BLANK]` |
| Legal / privacy reviewer (if required) | `[BLANK]` | `PENDING` | `[BLANK]` | `[BLANK]` |

**Authorization status:** `NOT AUTHORIZED` until all required approvals and the exact scope are recorded and independently checked.
