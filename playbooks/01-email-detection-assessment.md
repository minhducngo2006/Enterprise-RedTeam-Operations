# Email and Initial-Access Detection Assessment

> **Defensive-only; synthetic fixtures only.** This guide is for portfolio demonstration, not live operations. No real environment is accessed or tested. Do not place raw logs, account identities, secrets, customer data or production host information in this repository.

## 1. Objective

Demonstrate how a defensive assessment records the handling of a fictional suspicious-message alert. This guide assesses evidence quality and workflow traceability, not delivery or execution of a real phishing message.

## 2. Fixed control mapping

LAB-C002 — Alert Triage; LAB-C005 — Incident Escalation

## 3. Required synthetic inputs

- Synthetic mail-gateway verdict record
- Synthetic endpoint file-origin / process summary
- Synthetic user-report and SOC case record

All inputs must be explicitly labelled `source_kind: synthetic`. A missing fixture or missing field is not evidence of success.

## 4. Safe review procedure

1. Load only the bundled or separately authored synthetic event fixture; do not send email or access a real mailbox.
2. Check that the fixture contains a source label, timestamp, alert identifier and fictional asset alias.
3. Compare the recorded mail-gateway decision with the expected defensive disposition.
4. Review whether the fictional alert is assigned, triaged, closed or escalated with an accountable role.
5. Record any missing field as inconclusive or not_tested; do not infer successful detection.

## 5. Acceptance criteria

- [ ] The fixture is explicitly marked source_kind=synthetic.
- [ ] A relevant fictional alert has a traceable alert identifier and disposition.
- [ ] The triage record identifies an owner and review time.
- [ ] An escalation decision is recorded when the fictional severity criteria require it.

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

- No phishing infrastructure, message delivery, payload, attachment, HTML smuggling, credential capture or perimeter exploitation.
- No access to real mailboxes, users or production telemetry.

## 8. Remediation record

For a fictional `not_met` or `inconclusive` result, record a proposed owner role, corrective action, due-date placeholder and verification criterion. Do not mark remediation completed without a separate evidence reference and reviewer.

## 9. References

These official references provide defensive context only; they do not turn the synthetic fixture into a compliance assessment or prove control effectiveness. Reference review recorded 2026-11-25 in the preparation QA. Direct URL revalidation is pending where access was unavailable.

- NIST SP 800-61 Rev. 3, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* (final, April 2025): https://csrc.nist.gov/pubs/sp/800/61/r3/final. Used for incident-response preparation, detection, response and recovery context.
- CISA, *Enhance Email & Web Security* (CISA Insights): https://www.cisa.gov/sites/default/files/publications/CISAInsights-Cyber-EnhanceEmailandWebSecurity_S508C-a.pdf. Used for SPF, DKIM, DMARC, STARTTLS and HTTPS/HSTS defensive context.
