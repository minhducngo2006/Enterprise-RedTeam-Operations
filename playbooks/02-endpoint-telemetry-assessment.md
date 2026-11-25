# Endpoint Telemetry and Tamper-Resistance Assessment

> **Defensive-only; synthetic fixtures only.** This guide is for portfolio demonstration, not live operations. No real environment is accessed or tested. Do not place raw logs, account identities, secrets, customer data or production host information in this repository.

## 1. Objective

Demonstrate how endpoint protection health, telemetry continuity and response records are represented using fictional endpoint evidence.

## 2. Fixed control mapping

LAB-C002 — Alert Triage; LAB-C005 — Incident Escalation

## 3. Required synthetic inputs

- Synthetic endpoint health and policy-state record
- Synthetic tamper-protection administrative audit entry
- Synthetic process / image-load / script telemetry summary
- Synthetic EDR alert and SOC case record

All inputs must be explicitly labelled `source_kind: synthetic`. A missing fixture or missing field is not evidence of success.

## 4. Safe review procedure

1. Load only synthetic endpoint fixtures; do not connect to or modify an endpoint.
2. Check that endpoint policy assignment and protection-health fields are present.
3. Review the fictional telemetry summary for source, time, event category and endpoint alias.
4. Check whether the synthetic tamper-protection change has an authorized actor and audit record.
5. Verify that the corresponding fictional alert has a triage owner and escalation disposition.

## 5. Acceptance criteria

- [ ] The fixture records endpoint protection health and policy assignment.
- [ ] Telemetry records have source and time metadata.
- [ ] Security-setting changes are represented with an actor and audit trail.
- [ ] Alerts have an owner, disposition and escalation record.

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

- No unhooking, indirect syscalls, AMSI/ETW patching, process injection, masquerading, security-control bypass or C2 guidance.
- No endpoint access, policy changes or live validation.

## 8. Remediation record

For a fictional `not_met` or `inconclusive` result, record a proposed owner role, corrective action, due-date placeholder and verification criterion. Do not mark remediation completed without a separate evidence reference and reviewer.

## 9. References

These official references provide defensive context only; they do not turn the synthetic fixture into a compliance assessment or prove control effectiveness. Reference review recorded 2026-11-25 in the preparation QA. Direct URL revalidation is pending where access was unavailable.

- ASD's ACSC and international partners, *Best practices for event logging and threat detection* (published and reviewed 22 August 2024): https://www.cyber.gov.au/publication/best-practices-for-event-logging-and-threat-detection. Used for event-log policy, centralised collection, log quality, timestamp consistency and detection context.
- NIST SP 800-53 Rev. 5 control catalog, SI-4 System Monitoring (download page identifies current control-data version 5.1): https://csrc.nist.gov/projects/risk-management/sp800-53-controls/downloads. Used as background for system-monitoring context, not as a project compliance mapping.
