# Security Assessment & Defensive Evidence Toolkit

> An offline Python portfolio for educational Active Directory UserAccountControl (UAC) decoding and synthetic defensive-control evidence reporting.

**Publication status:** V2.1 portfolio published to public `main` under the owner's explicit authorization on 2026-11-25, despite the open historical-content and provenance items documented below. This is not a tagged/versioned release or a security clearance. The GitHub repository slug retains historical Red Team wording, but this candidate is defensive and offline. It does not run attacks or connect to enterprise systems.

## What is implemented

| Area | Capability | Entry point |
|---|---|---|
| Identity configuration | Decode one unsigned 32-bit UAC bitmask into named flags and educational risk indicators | `tools/ad_audit.py` |
| Defensive evidence | Validate a strict synthetic JSON schema against five fixed controls and calculate transparent status summaries | `tools/evidence_model.py` |
| Reporting | Render deterministic Markdown or JSON; optionally create a new output file without overwriting an existing path | `tools/evidence_report.py` |
| Assessment guidance | Four defensive review playbooks using synthetic fixtures only | `playbooks/` |
| Governance | Non-authorizing Rules of Engagement and blank evidence/deconfliction templates | `templates/` |

The two CLI flows are independent. The UAC decoder accepts one numeric mask; it is not a directory exporter, account dataset analyzer or live Active Directory auditor. The evidence scorecard reports statuses supplied by the input; it does not measure control effectiveness or verify evidence artifacts.

## Quickstart

**Requirements:** Python 3.11–3.14 (the configured CI support matrix). Runtime and tests use only the Python standard library; no package installation is required.

Run these commands from the repository root:

```bash
# Decode a sample UAC mask as JSON
python3 -B tools/ad_audit.py uac 4194816 --json

# Render the bundled synthetic evidence as Markdown
python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json

# Render the same data as JSON
python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json --format json

# Run the test suite
python3 -B -m unittest discover -s tests -v
```

To save a report, choose a new filename in an existing trusted directory:

```bash
python3 -B tools/evidence_report.py \
  --file examples/synthetic-evidence.json \
  --format markdown \
  --out ./synthetic-report.md
```

The report writer uses exclusive file creation: an existing file, symlink or directory is not overwritten. A partial file may remain if writing or closing fails; inspect it manually. Input and output paths must be trusted and stable. See the [CLI and file-handling contract](docs/evidence-schema.md).

## Evidence model

The scorecard contains exactly five fictional controls:

| ID | Control | Example criterion |
|---|---|---|
| LAB-C001 | Backup restoration | A synthetic restore exercise records a successful recovery |
| LAB-C002 | Alert triage | A synthetic alert record has an owner and disposition |
| LAB-C003 | Patch review | A synthetic patch review records an approved decision |
| LAB-C004 | Access review | A synthetic review records approval of a fictional access policy |
| LAB-C005 | Incident escalation | A synthetic exercise records an escalation decision |

Allowed statuses are `met`, `not_met`, `inconclusive` and `not_tested`. Only `met` and `not_met` count as evaluated. Omitted controls are reported separately and are not treated as a status.

The bundled [synthetic input](examples/synthetic-evidence.json) produces a [sample report](reports/synthetic-defensive-evidence.md): 3 of 5 submitted controls are evaluated (60.00% evaluation coverage); 2 of those 3 evaluated controls are met (66.67% met rate). These are illustrative schema metrics, not risk scores or proof of effectiveness. Evidence IDs such as `LAB-E001` are labels only, not artifact files, hashes or attestations.

Example outputs: [generated synthetic report](reports/synthetic-defensive-evidence.md) and [fictional control-assessment case study](reports/synthetic-defensive-control-assessment.md).

## Architecture

- [Architecture overview](docs/architecture.md) — the two CLI flows, module responsibilities and data path.
- [Project glossary](CONTEXT.md) — canonical terms for controls, statuses and synthetic evidence.
- [Evidence schema and CLI contract](docs/evidence-schema.md) — exact input shape, validation, exit codes and output behavior.
- [Limitations](docs/limitations.md) — explicit non-goals and trust assumptions.
- [Migration notes](docs/migration-v1-v2.md) — retirement of the legacy dataset `analyze` command.

## Defensive playbooks

These guides describe review of fictional records; they do not provide instructions to execute attacks or test real systems.

- [Email detection assessment](playbooks/01-email-detection-assessment.md) — LAB-C002, LAB-C005.
- [Endpoint telemetry assessment](playbooks/02-endpoint-telemetry-assessment.md) — LAB-C002, LAB-C005.
- [Identity and access review](playbooks/03-identity-access-review.md) — LAB-C004.
- [Remote-access hygiene](playbooks/04-remote-access-hygiene.md) — LAB-C004, LAB-C005.

The playbook set does not contain a dedicated guide for LAB-C001 Backup Restoration or LAB-C003 Patch Review. Those controls remain in the scorecard catalog, but no coverage should be inferred from another guide.

## Repository layout

```text
.
├── tools/       # UAC decoder, evidence model, report CLI
├── tests/       # unittest suite and golden report fixtures
├── examples/    # synthetic-only JSON input
├── reports/     # generated sample output and fictional case study
├── playbooks/   # defensive review guides
├── templates/   # non-authorizing governance templates
├── docs/        # architecture, schema, limitations, ADR and release gates
├── CONTEXT.md   # domain glossary
├── CONTRIBUTING.md
└── SECURITY.md
```

## Development and verification

See [Contributing](CONTRIBUTING.md) for the local workflow and code conventions.

- CI is configured for Linux and Python 3.11–3.14 in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
- The local candidate test suite has 45 tests. It was verified on Linux Python 3.11.18, 3.12.16, 3.13.15 and 3.14.7; Windows was not tested.
- Remote GitHub Actions status for the exact published commit must be checked before treating the CI matrix as verified; see the [release checklist](docs/release-checklist.md).

## Safety, limitations and release status

- Use independently fictional fixtures only. Never submit real identities, credentials, directory exports, security logs, host inventories, customer data or engagement artifacts.
- No live Active Directory, EDR, SIEM, endpoint, network or ticketing integration exists.
- No attack execution, credential collection, evasion, persistence, remote execution or production validation is implemented.
- UAC risk labels are educational heuristics, not verified security findings.
- Supplied evidence statuses are assertions; evidence IDs are labels, not verified artifacts.
- The Rules of Engagement document is a blank template, **not authorization**.
- This project is not an audit standard, compliance certification or production security product.

The owner expressly authorized direct publication to public `main` on 2026-11-25 despite the still-open historical F-01/F-10 content hygiene, F-02 provenance, independent security review and exact-SHA CI items. This limited exception does not rewrite history, close those gates, authorize a tag/formal release or establish security clearance. See [Security](SECURITY.md), [security disposition](docs/security-disposition.md) and the [release checklist](docs/release-checklist.md).

## License

No license has been selected or added. No reuse or redistribution permission is granted by this repository.
