# Synthetic evidence schema v1

Offline, synthetic fixtures only. This is not a real assessment or an audit standard. The fixed catalog in `tools/evidence_model.py` contains LAB-C001 Backup restoration, LAB-C002 Alert triage, LAB-C003 Patch review, LAB-C004 Access review, and LAB-C005 Incident escalation. Criteria describe fictional scenarios; statuses are supplied, not measured.

The input must be a JSON object with exactly three keys: `schema_version` (integer 1, not bool or float), `source_kind` (string "synthetic"), and `controls` (array of zero to five records). Each record has exactly `control_id`, `status`, and `evidence_id`. Control IDs must be unique and belong to the catalog. Evidence IDs are null or ASCII LAB-E followed by exactly three decimal digits (000–999); reuse is permitted.

| Status | Evidence ID |
| --- | --- |
| met | Required |
| not_met | Required |
| inconclusive | Null or ID |
| not_tested | Null only |

Evidence IDs are labels, not verified artifacts. There are no identity, host, network, credential, log or free-text fields. Exact keys and types reject extra containers. Omitted controls are not submitted outcomes.

See [limitations](limitations.md) for scope and [migration](migration-v1-v2.md) for legacy retirement.


## CLI and input boundary

Use `python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json [--format markdown|json] [--out PATH]` from the repository root. Markdown is the default. The input must be a regular nonsymlink file, at most 1,048,576 bytes (inclusive), UTF-8 without BOM. Duplicate JSON keys, NaN/Infinity, unexpected fields/types and extra nested containers are rejected. JSON is decoded before schema checking; there is no pre-parse depth guarantee, but recursion failures are handled as invalid evidence.

Exit 0 on success or help; exit 2 with fixed `Error: invalid arguments` for invalid CLI arguments; exit 1 with fixed `Error: invalid evidence`, `Error: input unavailable` or `Error: output unavailable` for the corresponding input/content/file-output error. These diagnostics are newline-terminated; invalid arguments and input/file-output errors do not echo data or paths and do not emit report stdout.

## Report contract

JSON output is not valid input. Output keys are schema_version, catalog_version, source_kind, summary and controls; rows include fixed title and criterion. Rows are sorted by control ID. Both formats use UTF-8 without BOM, LF and a trailing newline. No timestamps or environment data.

Evaluated = met + not_met. Evaluation coverage is 100 × evaluated / total submitted; met rate is 100 × met / evaluated. A zero denominator yields null in JSON and N/A in Markdown. Omitted = 5 − total submitted, separate from not_tested. Percentages are rounded to two decimal places. These are fictional scorecard metrics, not risk scores.

## Output boundary

Without --out, report bytes go to stdout. With --out, the full report is rendered first and then a new file is created exclusively. Existing paths, including the input itself, directories, hardlinks and symlinks, are rejected. Parent directories are not created. No automatic unlink: a partial file may remain on write or close failure. Use trusted local stable paths; no adversarial-concurrency, atomic visibility or crash-durability guarantee.

See the [example input](../examples/synthetic-evidence.json), [golden JSON](../tests/fixtures/synthetic-report.json) and [golden Markdown](../tests/fixtures/synthetic-report.md).
