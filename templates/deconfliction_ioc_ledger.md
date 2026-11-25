# Defensive Evidence & Deconfliction Register

> **Blank template — no activity is represented as performed.**
>
> All rows must be created for an approved exercise. Do not copy real hostnames, public IPs, user identities, credentials, customer data or raw logs into this repository. Use synthetic aliases and synthetic evidence-reference labels only.
>
> This human-readable governance register is not the strict V2.1 CLI JSON input. Only `control_id`, `status` and `evidence_id` map to a submitted `controls[]` record; `record_id`, asset alias, observation, timestamp, reviewer and cleanup fields remain outside that input schema.

## 1. Record metadata

| Field | Value |
|---|---|
| Exercise ID | `[REQUIRED]` |
| Source kind | `synthetic` |
| Catalog | `LAB-C001 through LAB-C005` |
| Register version | `1` |
| Record owner | `[BLANK]` |
| Reviewer | `[BLANK]` |
| Last reviewed (UTC) | `[BLANK]` |

## 2. Evidence register

| Record ID | Control ID | Asset alias | Observation (synthetic, concise) | Observed at (UTC) | Source kind | Evidence reference | Assessment status | Reviewer |
|---|---|---|---|---|---|---|---|---|
| `[UNASSIGNED]` | `[LAB-C00X]` | `[ASSET-ALIAS]` | `[NO OUTCOME — BLANK TEMPLATE ROW]` | `[BLANK]` | `synthetic` | `[LAB-E### — LABEL ONLY]` | `[BLANK — NOT SUBMITTED]` | `[BLANK]` |

Allowed submitted-control statuses: `met`, `not_met`, `inconclusive`, `not_tested`.

A blank template row is not a submitted record. Do not use `not_assessed` or `omitted` as control statuses. A control not submitted is absent from the submitted `controls[]` array and counted separately as omitted by the report.

A status must reflect the actual evidence available. Never pre-check a result or infer success from the absence of an alert.

## 3. Cleanup and closure

| Record ID | Cleanup required? | Cleanup status | Cleanup evidence reference | Verified by | Verified at (UTC) |
|---|---|---|---|---|---|
| `[UNASSIGNED]` | `unknown` | `not_assessed` | `[BLANK]` | `[BLANK]` | `[BLANK]` |

Allowed cleanup statuses: `not_assessed`, `pending`, `completed`, `not_applicable`, `failed`.

`completed` requires a traceable evidence reference and a named verifier. A blank cell is not equivalent to completed. No cleanup state is pre-populated as successful.

## 4. Provenance and handling rules

1. Every record belongs to one approved exercise ID and one control ID from the fixed catalog.
2. `source_kind` for repository examples is `synthetic`.
3. Evidence references are labels only; they do not represent artifact bytes, cryptographic hashes or independent attestations.
4. Real engagement evidence must remain in the organization's approved restricted evidence store, not in this repository.
5. Do not include passwords, tokens, private keys, raw event logs, real IP/host/user identifiers or customer records.
6. Keep observation, inference, inconclusive result and not-tested status distinct.
7. Record who reviewed each result and when; do not mark a record verified without an actual review.
8. If sensitive data is encountered, stop collection and follow the organization's incident/data-handling process.
