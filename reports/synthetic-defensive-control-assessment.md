# Synthetic Defensive Control Assessment — Example Services

Synthetic data — not evidence of a real engagement.

Statuses are supplied; evidence IDs are labels, not verified artifacts.

> **SYNTHETIC CASE STUDY — NOT A REAL ENGAGEMENT**
>
> **This is an illustrative data fixture, not a real engagement report.** Example Services, the environment, assets, scenario, observations, control outcomes and evidence-reference labels below are entirely fictional. No real organization or person is represented. No live system was accessed, tested, compromised or monitored. No credential was collected, recovered or used. No customer record was accessed or transferred. The reference labels are not evidence artifacts, hashes, logs or independent attestations.

## 1. Case study metadata

| Field | Value |
|---|---|
| Case study ID | SYN-CASE-001 |
| Source kind | synthetic |
| Design baseline | Security Assessment & Defensive Evidence Toolkit V2.1 (local candidate) |
| Assessment mode | Fictional tabletop / schema demonstration |
| Environment | Example Services — fictional |
| Domain | example.test (reserved example namespace) |
| Scope | Five fixed defensive controls, LAB-C001 through LAB-C005 |
| Evidence | Synthetic reference labels only; no artifact files |
| Verification | No real-world verification performed |

## 2. Purpose and limitations

This case study demonstrates how the toolkit records defensive-control outcomes, distinguishes evaluated controls from inconclusive or untested controls, and produces a transparent summary.

It does not demonstrate an actual security assessment, adversary emulation, production compromise, data access, exfiltration, detection efficacy or remediation success. It must not be used as audit evidence, a certification, a customer deliverable or proof of an organization's security posture.

## 3. Fictional scenario

Example Services is a fictional organization with a small demonstration environment containing:

- `ID-01.example.test` — fictional identity service;
- `APP-01.example.test` — fictional application service;
- `DB-01.example.test` — fictional database service;
- `BACKUP-01.example.test` — fictional backup service;
- `SOC-01.example.test` — fictional security-operations workflow.

The scenario assumes a routine defensive assurance exercise. It does not model or claim that an attacker accessed these systems. All observations are authored solely to exercise the evidence schema.

## 4. Fixed defensive control assessment

| Control ID | Defensive control | Fictional criterion | Status | Synthetic reference |
|---|---|---|---|---|
| LAB-C001 | Backup Restoration | Synthetic restore exercise records a successful recovery. | met | LAB-E001 |
| LAB-C002 | Alert Triage | Synthetic alert record documents an assigned owner and disposition. | met | LAB-E002 |
| LAB-C003 | Patch Review | Synthetic patch review records an approved remediation decision. | not_met | LAB-E003 |
| LAB-C004 | Access Review | Synthetic review records approval of a fictional access policy. | inconclusive | — |
| LAB-C005 | Incident Escalation | Synthetic exercise records a documented escalation decision. | not_tested | — |

**Reference semantics:** LAB-E001 through LAB-E003 are fictional labels used to illustrate schema linkage. They do not point to stored artifacts and do not have cryptographic hashes. Their presence is not proof that a test occurred.

## 5. Summary

| Measure | Fictional result |
|---|---:|
| Catalog controls | 5 |
| Submitted controls | 5 |
| Omitted controls | 0 |
| Met | 2 |
| Not met | 1 |
| Inconclusive | 1 |
| Not tested | 1 |
| Evaluated (met + not met) | 3 |
| Evaluation coverage (evaluated / submitted) | 60.00% |
| Met rate among evaluated (met / evaluated) | 66.67% |

Coverage is calculated only over submitted controls; omitted catalog controls are not assessed.

Inconclusive and not-tested controls are not counted as evaluated. Omitted controls, if any, must be reported separately and must not be silently treated as failures or passes. Omitted controls are absent from the submitted controls array; `omitted` is a summary count, not a submitted-control status. If a denominator is zero, the corresponding ratio is undefined and should be rendered as null / N/A.

## 6. Fictional observations and improvement opportunities

### LAB-C001 — Backup Restoration

The fictional scenario records a completed restore exercise and an integrity check of a sample dataset. This is a schema example only; it is not a real backup validation.

**Illustrative improvement:** retain restore-test ownership, scope, timing, integrity criteria and independent verification status in a real assessment system.

### LAB-C002 — Alert Triage

The fictional scenario records assignment, analyst review and closure of a simulated alert. No real alert or SOC workflow was accessed.

**Illustrative improvement:** record alert provenance, disposition rationale, escalation decision and review timestamp when a real, authorized assessment is performed.

### LAB-C003 — Patch Review

The fictional scenario records a missing approval and due-date decision for a high-priority patch. This is the only fictional control marked not_met.

**Illustrative improvement:** require an accountable owner, risk-based due date, exception approval and closure evidence.

### LAB-C004 — Access Review

The fictional sample does not include an explicit approval decision, approving role, policy version or review timestamp for the access policy. The criterion cannot be confirmed, so the result is inconclusive rather than a pass or fail.

**Illustrative improvement:** record the policy version, approving role, approval decision, review timestamp, scope and unresolved exceptions; maintain owner mapping as supporting context.

### LAB-C005 — Incident Escalation

No exercise is represented for this control. It is explicitly not_tested.

**Illustrative improvement:** schedule a safe tabletop exercise and capture the escalation decision, acknowledgement and post-exercise actions.

## 7. Data provenance and handling

- `source_kind`: `synthetic`.
- All entities, scenario details, statuses and reference labels are fictional.
- No real account names, passwords, tokens, personal data, host inventory, customer records, production metrics or raw logs are included.
- No real artifact is attached or implied.
- No result may be generalized to an actual organization's security posture.
- Any future real engagement must use a separately approved data-governance process and is outside this synthetic-only case study.

## 8. Conclusion

This case study demonstrates the intended reporting distinction between met, not-met, inconclusive and not-tested controls. It makes no claim that Example Services exists or that any assessment activity occurred.

**Publication condition:** this local revision is not authorization to publish or push the candidate. The owner separately attests that the F-01 credential-like value and F-10 placeholder were fictional and never used or reused in any real system; live credential rotation is not applicable on those attestations. The repository remains Public by explicit owner direction, and the historical F-01 report text and former Playbook 04 content remain in public `main` history. Original-report provenance remains UNKNOWN / UNVERIFIED, and history/public-copy review plus release approval remain pending. See [security disposition](../docs/security-disposition.md).
