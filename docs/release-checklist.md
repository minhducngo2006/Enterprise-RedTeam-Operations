# Release checklist

**Owner-approved publication exception (2026-11-25).** The owner expressly authorized publishing the V2.1 candidate to a feature branch and fast-forwarding `main` directly, without a pull request, despite the still-open historical-content, F-02 provenance, independent security-review and exact-SHA CI items below. This limited exception authorizes only the branch/main Git operations; it does not close those items, authorize history rewrite, tag or formal release, or constitute independent security clearance. Repository visibility remains Public.

## Local candidate verification (not release approval)

- [x] T1.3 migration: legacy `analyze` and dataset analyzer retired; scalar UAC decoder retained; two analyzer-specific tests retired; migration note and retirement test present.
- [x] Evidence schema and boundaries: fixed five-control schema v1, strict types/keys/statuses, 1 MiB input limit, duplicate-key/non-finite JSON rejection, nonsymlink regular-file input, exclusive new-file output and documented partial-file behavior.
- [x] Deterministic Markdown/JSON output matches both golden fixtures byte-for-byte; synthetic demo matches the Markdown golden fixture.
- [x] Full local unit suite: 45/45 on Linux Python 3.11.18, 3.12.16, 3.13.15 and 3.14.7; zero failures/skips on these runs. UAC and synthetic CLI smoke checks pass.
- [x] Post-standardization static audit: 20 Markdown files and 39 relative links (all resolve); 7 Python files parse; 2 JSON files parse; code fences are balanced; text files are UTF-8/LF with final newlines and no trailing whitespace; renamed paths have no stale references. Core/tests use only the standard library; no LICENSE or unsupported license badge.
- [ ] Windows not tested; remains best effort.
- [x] actionlint 1.7.12 (official release asset, SHA-256 verified) passes on `.github/workflows/ci.yml`.
- [ ] yamllint is unavailable; remote GitHub Actions for the final published `main` SHA is pending verification.
- [x] Gitleaks 8.30.1 (official release asset, SHA-256 verified) scanned all locally reachable refs (4 commits) and the current candidate working tree with 0 detections. This is not clearance: it does not classify known credential-like literals, prove absence of secrets, or enumerate forks/mirrors/caches/copies.
- [ ] Independent reviewer/security assessment not performed; current review is inline self-review only.

## Owner/security publication gates

- [x] F-01 owner attestation recorded: the credential-like value was fictional and never used or reused in a real system. Live AD/SQL rotation is not applicable on this attestation; it is not independent forensic verification.
- [ ] F-01 historical text/content hygiene reviewed across reachable history and public copies; any history rewrite requires separate explicit authorization. Repository visibility remains Public at the owner's explicit direction.
- [x] F-10 owner attestation recorded separately: the placeholder was fictional and never used or reused in any real system. Live credential rotation is not applicable on this attestation; it is not independent forensic verification.
- [ ] F-10 historical text/content hygiene reviewed across reachable history and public copies; any history rewrite requires separate explicit authorization.
- [ ] Original-report factual provenance remains UNKNOWN / UNVERIFIED unless supported by evidence. Synthetic replacement is clearly labelled; no unsupported claims or real data in the candidate.
- [ ] Final immutable SHA and remote CI evidence recorded for the published `main` commit; the owner-approved publication exception permits branch/main publication before this check is closed.
- [ ] Security-owner review of the local Gitleaks result, both owner attestations, F-01/F-10 historical content dispositions and downstream fork/mirror/cache/copy review completed.
- [ ] Linux CI matrix for Python 3.11, 3.12, 3.13 and 3.14 passes on that exact final SHA; Windows result or explicit skip is recorded.
- [x] Owner explicitly authorized feature-branch publication and direct fast-forward update of public `main` on 2026-11-25 despite the open items above. This is a limited exception, not closure of the remaining security/CI gates. No tag or formal release is authorized.

CI uses read-only repository contents permission and SHA-pinned checkout/setup-python, with no secrets, publishing or live assessment steps. Reviewed official action release tags, commit metadata and action manifests on 2026-11-25:
- [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) — `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- [actions/setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0) — `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`.
- [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use).

This is a review of release metadata and action interfaces, not an audit of bundled action code. Check the remote workflow run for the exact published `main` SHA before treating the CI matrix as verified.
