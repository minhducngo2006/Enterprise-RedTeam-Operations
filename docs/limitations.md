# Limitations

> This project is a published offline defensive evidence portfolio. It is not a live assessment service, attack platform, compliance certification or substitute for an authorized security engagement.

## 1. Synthetic-only evidence

The evidence model accepts synthetic-only records. Do not supply real account exports, identities, credentials, customer data, security logs, host inventories, certificates, packet captures or engagement artifacts.

A `source_kind: synthetic` field is a schema assertion, not independent proof that the data was created synthetically. The data owner remains responsible for ensuring that fixtures are independently fictional and contain no copied real values.

## 2. Fixed control catalog

The approved catalog contains exactly five controls:

- LAB-C001 — Backup restoration
- LAB-C002 — Alert triage
- LAB-C003 — Patch review
- LAB-C004 — Access review
- LAB-C005 — Incident escalation

The catalog is fixed and does not ingest user-defined controls, external control catalogs, executable tests, network data or host data.

## 3. Supplied status is not verified effectiveness

The allowed statuses are `met`, `not_met`, `inconclusive` and `not_tested`. A report describes supplied records; it does not independently test a control or verify an artifact.

Evidence IDs use the `LAB-E###` label format and are reference labels only. They are not verified links, hashes or attestations.

Omitted controls are reported separately and are not silently treated as met or not_tested. Inconclusive and not_tested controls are not counted as evaluated.

## 4. Score interpretation

Evaluation coverage is calculated over submitted controls only:

`100 × (met + not_met) / submitted`

The met percentage is calculated over evaluated controls only:

`100 × met / (met + not_met)`

Both values are null when their denominators are zero. A high percentage on a small subset does not mean the whole catalog was assessed. These values are not risk scores, compliance results or measures of real detection efficacy.

## 5. No live security operations

The product does not connect to live Active Directory, EDR, SIEM, endpoints, networks or ticketing systems. It does not execute attacks, collect credentials, perform persistence, conduct remote execution or validate controls against production systems.

## 6. Legacy retirement

The legacy dataset analyzer has been removed. The scalar UAC decoder is educational and does not verify account security. No live or dataset replacement is provided.

## 7. Runtime and platform support

Python 3.11–3.14 is the target. Linux CI is configured and Windows is best effort. Candidate development tests passed on Linux Python 3.11.18, 3.12.16, 3.13.15 and 3.14.7; Windows was not run. The remote GitHub Actions matrix passed on portfolio implementation commit `632c121c2b44d0a6d95399aa4491c439b23e8e0d` for Linux Python 3.11–3.14; subsequent commits must be checked separately. Core and tests are standard-library-only.

## 8. Local file boundary

Input is bounded to 1 MiB and regular nonsymlink files. Input and output paths must be trusted and stable. Output is exclusive creation; a failed write or close may leave a partial file for manual review. No overwrite, automatic unlink, sandbox, atomic visibility or race-proof guarantee. See [schema](evidence-schema.md).

## 9. Publication and license

The repository has no declared license. It remains Public at the owner's explicit direction. On 2026-11-25, the owner authorized direct publication of the V2.1 portfolio to public `main` despite the open historical-content, F-02 provenance and independent-review items; this limited exception is not a tagged/formal release or security clearance. The owner separately attests that the F-01 credential-like value and F-10 placeholder are fictional and were never used or reused in any real system, so live credential rotation is not applicable on those attestations. Historical text remains in reachable Git history and forks, mirrors, caches and downloaded copies have not been reviewed. The original report's factual provenance remains UNKNOWN / UNVERIFIED. See [security disposition](security-disposition.md) and [release checklist](release-checklist.md). No license or reuse permission is implied. Synthetic examples must not be presented as actual engagements, real incidents or validated customer outcomes.
