# Identity Privilege Hygiene and Directory Review

> **Defensive-only; synthetic fixtures only.** This guide is for portfolio demonstration, not live operations. No real environment is accessed or tested. Do not place raw logs, account identities, secrets, customer data or production host information in this repository.

## 1. Objective

Demonstrate how ownership and policy-review evidence for fictional directory identities is assessed without collecting secrets or using a real directory export.

## 2. Fixed control mapping

LAB-C004 — Access Review

LAB-C003 — Patch Review is not covered by this guide; reviewing directory policy or certificate-template settings is not a patch review.

## 3. Required synthetic inputs

- Synthetic privileged-group membership snapshot
- Synthetic service-identity owner and dependency register
- Synthetic authentication-policy summary
- Synthetic access-policy review record with policy version, approving role, decision and review timestamp
- Synthetic certificate-template configuration review record

All inputs must be explicitly labelled `source_kind: synthetic`. A missing fixture or missing field is not evidence of success.

## 4. Safe review procedure

1. Load only synthetic directory fixtures; never ingest a real Active Directory, LDAP or BloodHound export into this project.
2. Compare fictional privileged identities with the fixture's approved role/owner matrix.
3. Check whether each synthetic service identity has a named owner, business purpose and rotation-policy reference.
4. Review the fictional access-policy record for an explicit approval decision, approving role, policy version and review timestamp; review authentication-policy and certificate-template summaries for documented exceptions and approvals.
5. Record missing ownership or policy-approval evidence as inconclusive; do not attempt to obtain credentials or test privilege escalation.

## 5. Acceptance criteria

- [ ] The fictional access policy has a documented approval decision, approving role, policy version and review timestamp.
- [ ] Each fictional privileged identity has an accountable owner and business purpose.
- [ ] Service identities have a rotation-policy reference and dependency owner.
- [ ] Authentication-policy exceptions are documented and approved in the fixture.
- [ ] Configuration findings have an owner, risk, due date and review reference.

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

- No password/hash extraction, Kerberoasting, AS-REP hash collection/cracking, certificate impersonation, privilege escalation or directory exploitation.
- No real directory access or export.

## 8. Remediation record

For a fictional `not_met` or `inconclusive` result, record a proposed owner role, corrective action, due-date placeholder and verification criterion. Do not mark remediation completed without a separate evidence reference and reviewer.

## 9. References

These official references provide defensive context only; they do not turn the synthetic fixture into a compliance assessment or prove control effectiveness. Reference review recorded 2026-11-25 in the preparation QA. Direct URL revalidation is pending where access was unavailable.

- NIST SP 800-53 Rev. 5 control catalog (current derivative control-data version 5.1): AC-2 Account Management; AC-6(7) Review of User Privileges; IA-5 Authenticator Management. https://csrc.nist.gov/projects/risk-management/sp800-53-controls/downloads. Used for account ownership, privilege-review and authenticator-hygiene context.
- CISA, *Implementing Phishing-Resistant MFA* (October 2022): https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf. Used for phishing-resistant authentication context.
- Microsoft Learn, *Manage AD CS certificate templates on an enterprise CA*: https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/manage-certificate-templates. Used only as background for AD CS certificate-template administration: configuration, required management privileges, and the consequences of creating, deleting, renaming or deploying templates. This portfolio does not administer, publish, enroll from or change certificate templates.
