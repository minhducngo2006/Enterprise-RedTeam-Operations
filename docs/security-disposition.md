# Security Disposition — Owner Attestation and Public Visibility

Date: 2026-11-25 (Asia/Ho_Chi_Minh)
Repository: `minhducngo2006/Enterprise-RedTeam-Operations`
Reviewed public baseline: `main @ d269b92c17d8aea08bad6a6d18bf10692aff6e96`
V2.1 candidate: based on the reviewed baseline; owner-authorized for feature-branch publication and direct fast-forward update of `main` on 2026-11-25, despite the open items recorded below.

## 1. Owner instruction and visibility decision

The repository owner explicitly instructed that repository visibility must **remain Public**. No visibility setting was changed. On 2026-11-25, the owner separately authorized publishing the V2.1 portfolio candidate to a feature branch and updating `main` directly without a pull request, expressly accepting the still-open historical-content, F-02 provenance, independent security review and exact-SHA CI items. This is a limited publication exception, not independent security clearance, not authorization to rewrite history, and not approval for a versioned tag/release.

The owner confirmed that the F-01 credential-like value was entirely fictional and has never been used or reused in any real system. The owner reports that the personal lab has no Windows Server AD DS and no SQL Server. In a separate confirmation on 2026-11-25, the owner also confirmed that the F-10 placeholder was entirely fictional and has never been used or reused in any real system. Both are owner attestations recorded from the conversation; neither has been independently verified against external systems.

## 2. F-01 — disposition

**Classification: SYNTHETIC / NEVER USED OR REUSED — OWNER-ATTESTED.**

Based on this explicit owner attestation:
- The F-01 value is not treated as a live AD/SQL credential.
- AD/SQL rotation, revocation, dependency updates and session/ticket invalidation are **not applicable** to this owner-attested fictional value.
- No authentication attempt, production access, credential test or rotation was performed.

This closes the live-credential containment branch for F-01 on the owner's statement. It does not constitute independent forensic proof.

### Remaining F-01 repository hygiene

- Before this publication, public `main` pointed to `d269b92c17d8aea08bad6a6d18bf10692aff6e96` and its current tree included the historical report. The V2.1 tree replaces that report, but its old blob remains publicly reachable in Git history.
- The V2.1 tree replaces the old engagement report with a clearly synthetic defensive case study; this does not erase the old report from reachable history.
- The V2.1 commit does not rewrite reachable history or erase forks, mirrors, caches or downloaded copies; those copies have not been reviewed.
- A local Gitleaks 8.30.1 scan (official binary SHA-256 verified) covered all locally reachable refs and the current candidate working tree and reported zero detections. The scan does not independently verify either owner attestation, establish absence of other secrets, or cover forks, mirrors, caches or downloaded copies. Owner/security review and public-copy review remain open.
- The owner separately authorized a feature-branch commit/push and direct fast-forward update of `main` on 2026-11-25. No history rewrite, tag or formal release is authorized.

The repository remains Public by explicit owner choice. The historical text remains publicly reachable in Git history until a separately authorized content/history remediation is completed. The owner attestation says it is fictional and non-reused; do not misrepresent this as a confirmed live secret.

## 3. F-10 — separate owner-attested disposition

**Classification: SYNTHETIC / NEVER USED OR REUSED — OWNER-ATTESTED (separate from F-01).**

The owner separately confirmed on 2026-11-25 that the F-10 placeholder in the former Playbook 04 was entirely fictional and has never been used or reused in any real system. On that attestation:
- F-10 is not treated as a live credential.
- Credential rotation, revocation, dependency updates and session invalidation are not applicable to this owner-attested fictional placeholder.
- No authentication attempt, credential test, production access or rotation was performed.

This closes the live-credential containment branch for F-10 on the owner's statement. It is not independent forensic verification and does not resolve historical content hygiene.

The V2.1 tree removes the former Playbook 04 content; its historical blob remains publicly reachable in Git history. Review and remediation of reachable history, forks, mirrors, caches and downloaded copies remain open. Any history rewrite requires separate explicit authorization.

## 4. F-02 — original report provenance

The original engagement report's factual provenance remains **UNKNOWN / UNVERIFIED**. The F-01 attestation only addresses the origin and non-reuse of that one credential-like value; it does not verify the report's claims about Domain Admin access, production database access, customer records or exfiltration.

The approved D2 product decision replaces the unsupported report with the independently synthetic case study in the V2.1 tree. That replacement does not prove the old report was synthetic or real; the old report remains reachable in Git history.

## 5. Current gates

| Item | Status |
|---|---|
| F-01 live credential containment | **Closed by owner attestation; no live AD/SQL rotation applicable on that assertion** |
| F-01 historical text/content hygiene | **Open; public history/copies not remediated** |
| F-10 live credential containment | **Closed by separate owner attestation; no live credential rotation applicable on that assertion** |
| F-10 historical text/content hygiene | **Open; public history/copies not remediated** |
| F-02 original report factual provenance | **UNKNOWN / UNVERIFIED** |
| Repository visibility | **Public by explicit owner instruction; unchanged** |
| V2.1 portfolio publication | **Owner-authorized for feature branch and direct `main` update on 2026-11-25; no history rewrite or formal tag/release** |
| Local Gitleaks scan | **Run: 4 local commits and current tree, 0 detections; not clearance** |
| Owner/security review and public-copy review | **Pending** |
| Publication authorization | **Limited branch/main publication exception granted 2026-11-25; outstanding security/provenance/CI items remain open** |

## 6. Permission boundary

This document records the owner's attestations and limited publication exception. The owner authorized committing and pushing the portfolio candidate to a feature branch, then fast-forwarding public `main` directly without a pull request. This does not authorize history rewrite, tag, formal release, credential testing, production/identity/log access, or any claim that the open security/provenance gates are closed. Repository visibility remains Public.

No secret value is reproduced in this document.
