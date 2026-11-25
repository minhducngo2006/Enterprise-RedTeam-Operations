# Contributing

Thanks for helping improve the Security Assessment & Defensive Evidence Toolkit. Contributions must preserve its offline, synthetic-only scope.

## Requirements

- Python 3.11–3.14 (the configured CI support matrix).
- No third-party runtime or test dependencies are currently required.
- Run commands from the repository root.
- Do not install packages merely to run the current test suite.

## Local checks

Run the full unit suite:

```bash
python3 -B -m unittest discover -s tests -v
```

Run the CLI smoke checks:

```bash
python3 -B tools/ad_audit.py uac 512 --json
python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json --format json
python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json --format markdown
```

The two evidence-report outputs should match the committed golden files:

```bash
python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json --format json | cmp - tests/fixtures/synthetic-report.json
python3 -B tools/evidence_report.py --file examples/synthetic-evidence.json --format markdown | cmp - tests/fixtures/synthetic-report.md
```

## Code conventions

- Prefer the Python standard library; adding a dependency requires a concrete need and an explicit design decision.
- Keep the UAC decoder and synthetic evidence scorecard independent.
- Keep schema validation and summary calculations in the pure evidence model; keep filesystem access and CLI handling in the report module.
- Preserve deterministic report bytes and stable CLI exit/error behavior.
- Validate trust-boundary input explicitly. Do not echo submitted data or filesystem paths in generic error messages.
- Add `unittest` coverage for changed behavior, including relevant malformed-input and filesystem failure cases.
- Use descriptive names and type hints for module interfaces; keep four-space Python indentation, UTF-8 and LF line endings.
- Update the README, glossary, schema and limitations when a change affects the documented contract.

## Data and security rules

- Use independently fictional examples only.
- Never add real identities, passwords, tokens, directory exports, security logs, host inventories, customer data, packet captures or engagement artifacts.
- Do not add live integrations, attack execution, credential collection, evasion, persistence or remote-execution features to this project.
- Evidence IDs are labels only. Do not present them as hashes, verified artifacts or attestations.
- The Rules of Engagement file is a template, not authorization to access or test any system.

## Before opening a change

- [ ] The change stays within the offline synthetic-only scope.
- [ ] Tests and relevant CLI smoke checks pass.
- [ ] Golden outputs remain unchanged unless the report contract intentionally changes.
- [ ] Documentation and relative links match the implementation.
- [ ] No secret, personal data or production artifact has been added.
- [ ] Release and Git operations are separately authorized; a passing local test is not release approval.
