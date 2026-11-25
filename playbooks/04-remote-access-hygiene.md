# Remote-Access and Persistence-Hygiene Assessment

> **Defensive-only; synthetic fixtures only.** This guide is for portfolio demonstration, not live operations. No real environment is accessed or tested. Do not place raw logs, account identities, secrets, customer data or production host information in this repository.

## 1. Objective

Demonstrate how remote-administration access, privileged sessions and configuration-change monitoring are reviewed using fictional policy and audit fixtures.

## 2. Fixed control mapping

LAB-C004 — Access Review; LAB-C005 — Incident Escalation

## 3. Required synthetic inputs

- Synthetic remote-management policy snapshot
- Synthetic remote-management policy approval record (policy version, approving role, decision and review timestamp)
- Synthetic approved-admin membership list
- Synthetic service / scheduled-task / Group Policy change events
- Synthetic privileged-logon and incident-escalation records

All inputs must be explicitly labelled `source_kind: synthetic`. A missing fixture or missing field is not evidence of success.

## 4. Safe review procedure

1. Load only synthetic policy and audit fixtures; do not connect to a real endpoint or domain.
2. Review the fictional remote-management policy's approval decision, approving role, policy version and review timestamp; compare fictional remote-administration roles with the synthetic approved-owner list.
3. Review synthetic service, scheduled-task and policy-change records for an accountable change reference.
4. Check whether unexplained fictional changes have a triage owner, incident reference and escalation decision.
5. Record evidence gaps as inconclusive or not_tested; do not make changes to accounts, policies or services.

## 5. Acceptance criteria

- [ ] The fictional remote-management policy has a documented approval decision, approving role, policy version and review timestamp.
- [ ] Remote-administration access in the fixture is limited to approved fictional roles.
- [ ] Privileged sessions and configuration changes have audit references.
- [ ] Unexpected changes have a triage and escalation record.
- [ ] Exceptions and cleanup actions have evidence references and a reviewer.

For each submitted control record, use exactly `met`, `not_met`, `inconclusive` or `not_tested`. A control not submitted is absent from the `controls[]` array and counted separately as omitted; `omitted` is not a status value. Do not treat inconclusive or not-tested as evaluated.

## 6. Evidence metadata

- Exercise ID: `[SYN-CASE-ID]`
- Source kind: `synthetic`
- Control ID: `[LAB-C00X]`
- Evidence reference: `[LAB-E### — LABEL ONLY]`
- Reviewer / review time (UTC): `[REQUIRED]`
- Result and limitation: `[REQUIRED]`

Evidence-reference labels are not artifact files, hashes or independent attestations.

## 7. Prohibited activity

- No Pass-the-Hash, Overpass-the-Hash, WinRM/WMI remote execution, forged tickets, Golden Ticket, GPO/service persistence or lateral movement.
- No real remote sessions, policy changes or execution.

## 8. Remediation record

For a fictional `not_met` or `inconclusive` result, record a proposed owner role, corrective action, due-date placeholder and verification criterion. Do not mark remediation completed without a separate evidence reference and reviewer.

## 9. References

These official references provide defensive context only; they do not turn the synthetic fixture into a compliance assessment or prove control effectiveness. Reference review recorded 2026-11-25 in the preparation QA. Direct URL revalidation is pending where access was unavailable.

- CISA, NSA, FBI, MS-ISAC and INCD, *Guide to Securing Remote Access Software* (published 6 June 2023): https://www.cisa.gov/sites/default/files/2023-06/guide_to_securing_remote_access_software.pdf. Used for authorized-software inventory, configuration review, monitoring, least-privilege and segmentation context. Live-environment procedures remain outside this portfolio's scope.
- NIST SP 800-53 Rev. 5 control catalog (current derivative control-data version 5.1): AC-17 Remote Access, AC-6 Least Privilege and SI-4 System Monitoring. https://csrc.nist.gov/projects/risk-management/sp800-53-controls/downloads. Used as defensive context only.
- ASD's ACSC and international partners, *Best practices for event logging and threat detection* (22 August 2024): https://www.cyber.gov.au/publication/best-practices-for-event-logging-and-threat-detection. Used for event logging and detection context.
