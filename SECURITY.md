# Security policy

## Scope and safe use

This project is an offline educational toolkit: a scalar UAC bitmask decoder and a fixed synthetic defensive evidence scorecard. It does not perform live assessment, collect credentials, execute attacks or validate actual control effectiveness. Use independently fictional inputs only. Do not submit production data, credentials, identities or logs.

## Reporting

No private reporting channel or security contact has been verified. Contact the repository owner through an established private channel; confirm the recipient before sharing any sensitive material. If no private channel can be established, do not post secrets, real artifacts or reproduction data publicly. A public issue, if available, should contain only a minimal non-sensitive description.

Report the affected version or commit, expected versus observed behavior, impact and a minimal synthetic reproduction. Do not test credentials or systems without separate authorization. The owner should triage, contain and coordinate remediation, recording non-sensitive evidence.

## Known disclosure and publication status

The repository remains **Public** at the owner's explicit direction; no visibility setting was changed. The owner separately attests that the F-01 credential-like value and F-10 placeholder were fictional and never used or reused in any real system. Live credential rotation is not applicable on these attestations; they are not independent forensic verification. The V2.1 tree replaces the old F-01 report and former Playbook 04 content, but their historical blobs remain publicly reachable in Git history; forks, mirrors, caches and downloaded copies have not been reviewed.

The original engagement report's factual provenance remains UNKNOWN / UNVERIFIED; the synthetic replacement does not validate the old report's claims. A local Gitleaks 8.30.1 scan of four locally reachable commits and the candidate working tree reported zero detections; it does not independently verify either attestation or cover forks, mirrors, caches or downloaded copies. The owner authorized direct publication to public `main` on 2026-11-25 despite the open F-01/F-10 historical-content hygiene, F-02 provenance, security-owner review and public-copy review items. This limited exception is not a security clearance or a tagged/formal release. See [security disposition](docs/security-disposition.md), [release checklist](docs/release-checklist.md) and [limitations](docs/limitations.md).

Python 3.11–3.14 is the target, with Linux CI and best-effort Windows. Local tests pass on Linux Python 3.11.18, 3.12.16, 3.13.15 and 3.14.7; Windows is untested. Remote CI and compatibility for the exact final authorized SHA remain unverified. No release support window or license has been established.
